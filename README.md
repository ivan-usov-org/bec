# BEC 

Beamline Experiment Control (BEC)


## Documentation

The documentation is hosted here: https://beamline-experiment-control.readthedocs.io/

## Contributing

All commits should use the Angular commit scheme:

> #### <a name="commit-header"></a>Angular Commit Message Header
> 
> ```
> <type>(<scope>): <short summary>
>   │       │             │
>   │       │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
>   │       │
>   │       └─⫸ Commit Scope: animations|bazel|benchpress|common|compiler|compiler-cli|core|
>   │                          elements|forms|http|language-service|localize|platform-browser|
>   │                          platform-browser-dynamic|platform-server|router|service-worker|
>   │                          upgrade|zone.js|packaging|changelog|docs-infra|migrations|ngcc|ve|
>   │                          devtools
>   │
>   └─⫸ Commit Type: build|ci|docs|feat|fix|perf|refactor|test
> ```
> 
> The `<type>` and `<summary>` fields are mandatory, the `(<scope>)` field is optional.

> ##### Type
> 
> Must be one of the following:
> 
> * **build**: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
> * **ci**: Changes to our CI configuration files and scripts (examples: CircleCi, SauceLabs)
> * **docs**: Documentation only changes
> * **feat**: A new feature
> * **fix**: A bug fix
> * **perf**: A code change that improves performance
> * **refactor**: A code change that neither fixes a bug nor adds a feature
> * **test**: Adding missing tests or correcting existing tests
