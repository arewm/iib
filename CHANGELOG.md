# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 6.7.2
- Fix bundle_replacements bug when the user doesn't provide it in regenerate-bundle requests

## 6.7.1
- Fix dev env compose files
- Fix bundle_replacements bug in regenerate-bundle request
- Upgrade OPM to 1.26.2 in dev env
- Fix buildah bud command retries
- Adding retry and port check when opm serve/opm registry serve is called

## 6.7.0
- Add bundle_replacements parameter to regenerate_bundle API and worker
- Bump mako version
- Increase iib_api_timeout to 120 seconds
- Fix RM request private registry bug

## 6.6.1
- Add recursive-related-bundles endpoint 
- Adding ability to create single-active-consumer queues
- Add static types and mypy checks
- Append overwrite index token to current docker config.

## 6.5.0
- Print version of binary files in log files
- Improve traceability in _get_present_bundles and fix tests
- Increase iib_api_timeout, iib_retry_delay and iib_retry_jitter
- Keep Gating feature in IIB and improve gating logging
- Adding fallback from SIGTERM to SIGKILL
- Fix dependency issues for python 3.9

## 6.4.0
- Add internal_index_image_copy and internal_index_image_copy_resolved to Add and Rm response
- Add a warning for when gating is disabled

## 6.3.0
- Fix create-empty-index endpoint to not accept build_tags
- Update black to stable version 22.3.0
- Build container image for message broker and push to quay.io
- Upgrade OPM to 1.21.0
- Remove FIXME comments for issues caught by bandit
- Bump pytest from 7.1.0 to 7.1.2 

## 6.2.0
- Fix bug of missing related_bundles param and logs param in API response
- Modify permissions on logs files 

## 6.1.0 
- Add support for Python3.9
- Enable send events to the broker
- Bump pytest from 6.2.5 to 7.0.0
- Use terminate function to shut down a process instead of kill
- Pretty print (log) of RequestConfig classes
- Logging improvements

## 6.0.2
- Added support for File-Based Catalog
- Dropped support for Python3.6
- Fixed bug for failing opm index deprecatetruncate
- Fixed loosing olm.maxOpenShiftVersion property
- Fixed bug for Buildah retries on 5XX
- Added Static Application Security Testing
- Updated Celery to 5.2.2 for Python 3.8
- Fixed mod_wsgi package in iib-api

## 5.0.0
 - Fix issue of deprecation list with duplicated bundles
 - Add mod_wsgi dependency to Dockerfile-api
 - Update opm in dev env to v1.19.5
 - Add framework to support FBC indexes
 - Upgrade Flask 2.0.2, Werkzeug 2.0.2, Celery 5.1.2, Kombu 5.1.0
 - Add support for Python 3.8
 - Add retries and minor fixes for buildah commands
 - Add REGISTRY_AUTH_FILE support in dev env
 - Add support for AWS S3 buckets for artifacts storage
 - Add github action to build API image on tag push

## 4.9.0
 - Fix the comparison of index image and bundle
 - Avoid failing to create-empty-index when labels are not set
 - Generate registry certificates automatically for dev env
 - Remove x509ignoreCN workaround
 - Update OPM, grpcurl and operator-sdk in dev-env

## 4.8.0
- pinning is now a customization. If customization is used for an organization, it will not be
  done automatically unless explicitly specified
- renamed Declarative Config to File Based Config
- added support for filtering on user, request_type and index_image on builds endpoint

## 4.7.0
- having relatedImages and RELATED_IMAGES_* in the bundle image is now valid for regeneration
- fixed inconsistencies in arch selection code for different endpoints

## 4.6.2
- Attempt adding maxOpenshiftVersion property only when adding bundles to index

## 4.6.1
- fixed bug to use registry token while inspecting image

## 4.6.0
- added build and push iib-worker and iib-api images to quay.io
- fixed bug to clean local manifest lists before creating a new one
- used ubi8 as base images for api and worker
- fixed merge-index-image bug that created the same manifest list twice
- added setting OcpMaxVersion property in merge-index-image
- added new attribute 'build_tags' for index_image operations
- bumped pytest-cov from 2.12.1 to 3.0.0
- bumped coverage from 5.5 to 6.0.1

## 4.5.0
- replaced manifest-tool with buildah to build manifest lists
- added declarative config migrator to worker dockerfile

## 4.4.1
- fixed merge-index-image bugs
- fixed deprecatetruncate command

## 4.4.0
- deprecated legacy support for OMPS

## 4.3.0
- fixed memcached key length error
- fixed registry_auth in batch regenerate-bundle requests
- added related_bundles api endpoint for regenerate-bundle requests

## 4.2.0
- Add create-empty-index functionality
- Replace custom retry with retry package and setting backoff interval for skopeo_inspect
- Set --arch when building images
- Bump pytest-cov from 2.12.0 to 2.12.1
- Remove retry delay during tests
- Request and urllib3 update
- Use pinned runtime requirements in tests
- Fix apply_repo_enclosure bug when namespace is None

## 4.1.0
- removed support for privileged users
- added retries for OMPS pushes
- fixed bug in merge-index-image endpoint to deprecate invalid bundles instead of filtering them
- added functionality to add olm.maxOpenShiftVersion property to bundles being added

## 4.0.0
- fixed use of token when inspecting source and target indexes in merge-index-image endpoint
- added support for substitutes-for functionality supported in OPM 1.17.0
- upgraded py from 1.9.0 to 1.10.0
- changed format of iib_organization_customizations to make it more generic
- fixed bug to re-add labels to indexes if deprecation is run in add requests
- upgraded pytest from 6.2.3 to 6.2.4
- fixed a bug where a variable isn't assigned in handle_add_request
- fixed bug to preserve double quotes when parsing YAML files in regenerate-bundle
- added support for image_name_from_labels and enclose_repo customizations in regenerate-bundle

## 3.11.2
- fixed bug to filter unique bundles from listBundles response
- added support for private registry pull secrets to regenerate bundle requests
- added podman container-tool when merging indexes
- upgraded pytest from 6.2.2 to 6.2.3
- upgraded opm in dev environment to v1.16.1
- fixed skopeo pull to retry when mediatype is none
- fixed index_image_resolved bug for merge index image endpoint
- fixed ocp_version range filter
- stopped setting content-encoding on AMQP messages

## 3.11.1
- fixed bugs for deprecating bundles in add requests
- upgraded cryptography from 3.3.1 to 3.3.2
- upgraded jinja2 from 2.11.1 to 2.11.3
- added new attribute index_image_resolved to add and rm response

## 3.11.0
- fixed docker-compose quirks
- added support for parsing bundle version in merge-index-image before adding it to the index
- added better error handling for regenerate-bundle requests
- added support for deprecation list in add requests

## 3.10.1
- fix distribution_scope bug

## 3.10.0
- added propagation of validated distribution_scope
- added ability to turn on caching for skopeo inspect of images with same digest
- updated API documentation

## 3.9.2
### Added
- Ignoring duplicate bundles in payload for add operator request
