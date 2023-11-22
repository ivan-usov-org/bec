## Contributing

Thank you for considering contributing to BEC! Contributions are essential for improving the project and helping it grow. We welcome your bug reports, feature requests, documentation improvements, and code contributions.

### How to Contribute

#### Reporting Bugs or Requesting Features:

- Before submitting a bug report or feature request, please check the [issue tracker](https://gitlab.psi.ch/bec/bec/issues) to avoid duplication.
- If the issue or feature hasn't been reported, open a new issue with a clear title and description. Be sure to provide steps to reproduce for bugs.

#### Contributing Code:

1. Create a new branch for your changes:

    ```bash
    git checkout -b feature/your-feature
    ```

2. Make your changes.

3. Use Black to format your code:

    ```bash
    black --line-length=100 --skip-magic-trailing-comma --experimental-string-processing .
    ```

4. Run Pylint on your code to ensure it meets coding standards:

    ```bash
    pylint your_module_or_package
    ```

5. Write tests for new features or fixed bugs.

6. Follow [Conventional Commit Messages](https://www.conventionalcommits.org/en/v1.0.0/) when writing commit messages. This helps us automatically generate a changelog. For example:

    ```bash
    git commit -m "feat: add new feature"
    ```

    or

    ```bash
    git commit -m "fix: fix bug"
    ```

    or

    ```bash
    git commit -m "docs: update documentation"
    ```

7. Push your commits to the remote branch:

    ```bash
    git push origin feature/your-feature
    ```

8. Open a merge request on GitLab. Be sure to include a clear title and description of your changes. If your merge request fixes an issue, include `closes #123` in the description to automatically close the issue when the merge request is merged.

#### Contributing Documentation:

- Improvements to documentation are always appreciated! If you find a typo or think something could be explained better, please open an issue or merge request.
- If you are adding new documentation, please follow the same steps as contributing code above.