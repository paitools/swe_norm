from nomad.config.models.north import NORTHTool
from nomad.config.models.plugins import NorthToolEntryPoint

swe_north_tool = NORTHTool(
    short_description='Jupyter Notebook server in NOMAD NORTH for NOMAD plugin swe_norm.',
    image='ghcr.io/foo/swe_norm:main',
    description='Jupyter Notebook server in NOMAD NORTH for NOMAD plugin swe_norm.',
    external_mounts=[],
    file_extensions=['ipynb'],
    icon='logo/jupyter.svg',
    image_pull_policy='Always',
    default_url='/lab',
    maintainer=[{'email': 'ivanovip@hsu-hh.de', 'name': 'Pavle Ivanovic'}],
    mount_path='/home/jovyan',
    path_prefix='lab/tree',
    privileged=False,
    with_path=True,
    display_name='swe_north_tool',
)

north_entry_point = NorthToolEntryPoint(
    id_url_safe='swe-module-swe-north-tool',
    north_tool=swe_north_tool,
)
