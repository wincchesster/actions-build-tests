# Lesson-25-26. GitHub Actions. Docker
This project demonstrates the usage of GitHub Actions for automated build, testing, and deployment workflows. The main workflow is defined in the **build-and-push.yml file**. It is triggered on every push to the main branch.


## Workflow Overview
* **Checkout Repository**: Checks out the source code from the repository.
* **Log in to the Container registry**: Uses Docker login action to log in to the specified container registry (ghcr.io in this case) using the provided GitHub token.
* **Extract Metadata**: Utilizes Docker metadata action to extract metadata such as tags and labels for Docker images.
* **Bump Version and Push Tag**: Uses the GitHub tag action to bump the version and push a new tag to the repository.
* **Build Image**: Builds the Docker image without pushing it. Tags include the new version and latest.
* **Build Image with Tests**: Builds another Docker image specifically for tests.
* **Run Tests**: Runs tests using the docker-compose command.
* **Push Image**: Pushes the Docker image with the new version tag and latest to the container registry.
* **Test Coverage**: Runs tests for code coverage.
* **Push Coverage**: Commits and pushes the code coverage report to the gh-pages branch.
* **Deploy to GitHub Pages**: Deploys the code coverage report to GitHub Pages.
* **Archive Code Coverage Results**: Archives the code coverage report as an artifact.
* **Create GitHub Release**: Creates a GitHub release with the code coverage report as an attachment and specified release notes.


## build-and-push.yml

```sh
name: Build

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4


      - name: Log in to the Container registry
        uses: docker/login-action@65b78e6e13532edd9afa3aa52ac7964289d1a9c1
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

    
      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@9ec57ed1fcdbf14dcef7dfbe97b2010124a938b7
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
    
      - name: Bump version and push tag
        id: tag_version
        uses: mathieudutour/github-tag-action@v6.1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}

    # if you want to use the this function you need change IMAGE_NAME to REPO in next step .    
    #   - name: downcase REPO name
    #     run: |
    #         echo "REPO=${GITHUB_REPOSITORY,,}" >>${GITHUB_ENV}

      - name: Build image
        uses: docker/build-push-action@v5
        with:
          push: false
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.tag_version.outputs.new_tag }}, ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest

      - name: Build image with tests
        uses: docker/build-push-action@v5
        with:
          file: Dockerfile_tests
          push: false
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:tests
      
      - name: Run tests
        id: run_tests
        run: |
          docker compose up -d mysql
          docker compose up --exit-code-from python_testing_app python_testing_app
          

      - name: Push image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.tag_version.outputs.new_tag }}, ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest


      - name: Test coverage
        run: |
          mkdir coverage
          docker compose up -d mysql
          docker compose up app-coverage
          rm -rf coverage/.gitignore


      - name: Push coverage
        uses: EndBug/add-and-commit@v9
        with:
          author_name: Oleksander Chaikovskyi
          author_email: wincchesster@gmail.com
          message: 'Add code coverage report'
          add: 'coverage'
          new_branch: gh-pages 
          push: true
        

      - name: Deploy to GitHub Pages
        uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: gh-pages # is default and can be changed to another branch
          build_dir: coverage
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}


      - name: Archive code coverage results
        uses: actions/upload-artifact@v3
        with:
          name: code-coverage-report
          path: coverage/index.html


      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: coverage/index.html
          body: |
            Some release notes go here.
          tag_name: ${{ steps.tag_version.outputs.new_tag }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Usage
To use this workflow, follow these steps:

* Push changes to the **main** branch or create a pull request.
* GitHub Actions will automatically trigger the workflow.
* View the workflow progress and results in the Actions tab of your GitHub repository.
* Once the workflow is complete, check the GitHub Releases section for the newly created release.
* The code coverage report is available on the **gh-pages** branch and GitHub Pages. (https://wincchesster.github.io/actions-build-tests/)



## Result
<img src="https://i.imgur.com/paSO0qV.png" alt="drawing" width="95%"/></img>
<img src="https://i.imgur.com/ofS1E1s.png" alt="drawing" width="95%"/></img>
_____________________________________________________
> **Note:** The workflow is triggered on every push to the main branch. To trigger the workflow manually, click the **Run workflow** button in the Actions tab of your GitHub repository.








