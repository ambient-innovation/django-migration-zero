from ambient_package_update.metadata.author import PackageAuthor
from ambient_package_update.metadata.constants import (
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
            name="Ambient Digital",
            email="hello@ambient.digital",
        ),
    ],
    maintainer=PackageMaintainer(name="Ambient Digital", url="https://ambient.digital/", email="hello@ambient.digital"),
    licenser="Ambient Innovation: GmbH",
    license=LICENSE_MIT,
    license_year=2023,
    development_status="5 - Production/Stable",
    has_migrations=True,
    claim='Holistic implementation of "migration zero" pattern for Django covering local changes and '
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
