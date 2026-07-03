from ambient_package_update.metadata.author import PackageAuthor
from ambient_package_update.metadata.constants import (
    DEPLOYMENT_STATUS_STABLE,
    DEV_DEPENDENCIES,
    LICENSE_MIT,
    SUPPORTED_DJANGO_VERSIONS,
    SUPPORTED_PYTHON_VERSIONS,
)
from ambient_package_update.metadata.maintainer import PackageMaintainer
from ambient_package_update.metadata.package import PackageMetadata
from ambient_package_update.metadata.readme import ReadmeContent
from ambient_package_update.metadata.ruff_ignored_inspection import RuffIgnoredInspection

METADATA = PackageMetadata(
    package_name="django-migration-zero",
    github_package_group="ambient-innovation",
    authors=[
        PackageAuthor(
            name="Beyonder Deutschland",
            email="hello@beyonder.de",
        ),
    ],
    maintainer=PackageMaintainer(name="Beyonder Deutschland", url="https://beyonder.de/", email="hello@beyonder.de"),
    licenser="Beyonder Deutschland GmbH",
    license=LICENSE_MIT,
    license_year=2023,
    development_status=DEPLOYMENT_STATUS_STABLE,
    has_migrations=True,
    claim="Holistic implementation of 'migration zero' pattern for Django covering local changes and "
    "in-production database adjustments.",
    readme_content=ReadmeContent(uses_internationalisation=True),
    dependencies=[
        f"Django>={SUPPORTED_DJANGO_VERSIONS[0]}",
    ],
    supported_django_versions=SUPPORTED_DJANGO_VERSIONS,
    supported_python_versions=SUPPORTED_PYTHON_VERSIONS,
    optional_dependencies={
        "dev": [*DEV_DEPENDENCIES, "unittest-parametrize~=1.3", "freezegun~=1.5"],
    },
    ruff_ignore_list=[
        RuffIgnoredInspection(key="TRY003", comment="Avoid specifying long messages outside the exception class"),
    ],
)
