# SPDX-License-Identifier: GPL-3.0-or-later
from datetime import timedelta
from unittest import mock

import pytest

from iib.exceptions import ValidationError
from iib.web import models


def test_request_add_architecture(db, minimal_request):
    minimal_request.add_architecture('amd64')
    minimal_request.add_architecture('s390x')
    db.session.commit()
    assert len(minimal_request.architectures) == 2
    assert minimal_request.architectures[0].name == 'amd64'
    assert minimal_request.architectures[1].name == 's390x'

    # Verify that the method is idempotent
    minimal_request.add_architecture('amd64')
    db.session.commit()
    assert len(minimal_request.architectures) == 2


def test_request_add_tag(db, minimal_request):
    binary_image = models.Image(pull_specification='quay.io/add/binary-image:latest2')
    db.session.add(binary_image)
    batch = models.Batch()
    db.session.add(batch)
    request = models.RequestAdd(batch=batch, binary_image=binary_image)
    db.session.add(request)
    db.session.commit()
    minimal_request.add_build_tag('build-tag1')

    minimal_request.add_build_tag('build-tag1')
    minimal_request.add_build_tag('build-tag1')
    minimal_request.add_build_tag('build-tag2')
    db.session.commit()
    assert len(minimal_request.build_tags) == 2
    assert minimal_request.build_tags[0].name == 'build-tag1'
    assert minimal_request.build_tags[1].name == 'build-tag2'


def test_request_add_state(db, minimal_request):
    minimal_request.add_state('in_progress', 'Starting things up')
    minimal_request.add_state('complete', 'All done!')
    db.session.commit()

    assert len(minimal_request.states) == 2
    assert minimal_request.state.state_name == 'complete'
    assert minimal_request.state.state_reason == 'All done!'
    assert minimal_request.states[0].state_name == 'in_progress'
    # Ensure that minimal_request.state is the latest state
    assert minimal_request.state == minimal_request.states[1]


def test_request_add_state_invalid_state(db, minimal_request):
    with pytest.raises(ValidationError, match='The state "invalid" is invalid'):
        minimal_request.add_state('invalid', 'Starting things up')


@pytest.mark.parametrize('state', ('complete', 'failed'))
def test_request_add_state_already_done(state, db, minimal_request):
    with pytest.raises(ValidationError, match=f'A {state} request cannot change states'):
        minimal_request.add_state(state, 'Done')
        db.session.commit()
        minimal_request.add_state('in_progress', 'Oops!')


def test_request_temporary_data_expiration(app, db, minimal_request):
    minimal_request.add_state('in_progress', 'Starting things up')
    db.session.commit()
    app.config['IIB_REQUEST_DATA_DAYS_TO_LIVE'] = 99
    updated = minimal_request.state.updated
    assert minimal_request.temporary_data_expiration == (updated + timedelta(days=99))


def test_get_state_names():
    assert models.RequestStateMapping.get_names() == ['complete', 'failed', 'in_progress']


def test_get_type_names():
    assert models.RequestTypeMapping.get_names() == [
        'add',
        'create_empty_index',
        'generic',
        'merge_index_image',
        'recursive_related_bundles',
        'regenerate_bundle',
        'rm',
    ]


@pytest.mark.parametrize(
    'type_num, is_valid',
    [
        (0, True),
        (1, True),
        (2, True),
        (3, True),
        (4, True),
        (5, True),
        (6, True),
        (7, False),
        ('1', False),
        (None, False),
    ],
)
def test_request_type_validation(type_num, is_valid):
    if is_valid:
        models.Request(type=type_num)
    else:
        with pytest.raises(ValidationError, match=f'{type_num} is not a valid request type number'):
            models.Request(type=type_num)


def test_batch_user(db, minimal_request_add, minimal_request_rm):
    minimal_request_add.user = models.User(username='han_solo@SW.COM')
    minimal_request_rm.user = models.User(username='yoda@SW.COM')
    db.session.commit()

    assert minimal_request_add.batch.user.username == 'han_solo@SW.COM'
    assert minimal_request_rm.batch.user.username == 'yoda@SW.COM'


@pytest.mark.parametrize('last_request_state', ('in_progress', 'failed', 'complete'))
def test_batch_state(last_request_state, db):
    binary_image = models.Image(pull_specification='quay.io/add/binary-image:latest')
    db.session.add(binary_image)
    batch = models.Batch()
    db.session.add(batch)
    for i in range(3):
        request = models.RequestAdd(batch=batch, binary_image=binary_image)
        request.add_state('complete', 'Some reason')
        db.session.add(request)

    request = models.RequestAdd(batch=batch, binary_image=binary_image)
    request.add_state(last_request_state, 'Some reason')
    db.session.add(request)
    db.session.commit()

    assert request.batch.state == last_request_state


def test_batch_request_states(db):
    binary_image = models.Image(pull_specification='quay.io/add/binary-image:latest')
    db.session.add(binary_image)
    batch = models.Batch()
    db.session.add(batch)
    for state in ('in_progress', 'failed', 'complete'):
        request = models.RequestAdd(batch=batch, binary_image=binary_image)
        request.add_state(state, 'Some state')
        db.session.add(request)

    db.session.commit()

    assert request.batch.request_states == ['in_progress', 'failed', 'complete']


@pytest.mark.parametrize(
    'registry_auths, msg_error',
    (
        ([{'registry.redhat.io': {'auth': 'YOLO'}}], '"registry_auths" must be a dict'),
        (
            {
                'auths': {'registry.redhat.io': {'auth': 'YOLO'}},
                'foo': {'registry.redhat.stage.io': {'auth': 'YOLO2'}},
            },
            '"registry_auths" must contain single key "auths"',
        ),
        ({'auths': {}}, '"registry_auths.auths" must be a non-empty dict'),
        (
            {'auths': {'registry': {'authS': 'YOLO'}}},
            'registry in registry_auths has auth value in incorrect format. '
            'See the API docs for details on the expected format',
        ),
        (
            {'auths': {'registry': ['auth', 'YOLO']}},
            'registry in registry_auths has auth value in incorrect format. '
            'See the API docs for details on the expected format',
        ),
        (
            {'auths': {'registry': {'auth': 'YOLO', 'foo': 'YOLO2'}}},
            'registry in registry_auths has auth value in incorrect format. '
            'See the API docs for details on the expected format',
        ),
    ),
)
def test_validate_registry_auths(registry_auths, msg_error):
    with pytest.raises(ValidationError, match=msg_error):
        models.validate_registry_auths(registry_auths)


@mock.patch('iib.web.models.url_for')
def test_request_logs_and_related_bundles_in_response(
    mock_url_for, app, db, minimal_request_regenerate_bundle
):
    mock_url_for.return_value = 'some-url-for-data'
    minimal_request_regenerate_bundle.add_state('in_progress', 'Starting things up')
    db.session.commit()
    app.config['IIB_AWS_S3_BUCKET_NAME'] = 'some_bucket'
    app.config['IIB_REQUEST_LOGS_DIR'] = None
    app.config['IIB_REQUEST_RELATED_BUNDLES_DIR'] = None

    rv = minimal_request_regenerate_bundle.to_json(verbose=True)
    assert rv['logs']['url'] == 'some-url-for-data'
    assert rv['related_bundles']['url'] == 'some-url-for-data'
    assert rv['bundle_replacements'] == {}
