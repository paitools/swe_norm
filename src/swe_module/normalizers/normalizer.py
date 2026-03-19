from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger

import yaml
from nomad.config import config
from nomad.normalizing import Normalizer

from electronicparsers.vasp.metainfo.surface import (
    section_surface_metadata,
    section_surface_site,
)

configuration = config.get_plugin_entry_point(
    'swe_module.normalizers:normalizer_entry_point'
)


class SurfaceNormalizer(Normalizer):
    def normalize(self, archive: 'EntryArchive', logger: 'BoundLogger') -> None:
        super().normalize(archive, logger)

        # Try to locate surface.yaml inside the uploaded files
        try:
            yaml_path = archive.m_context.raw_path('surface.yaml')
        except Exception:
            logger.info('SurfaceNormalizer: no surface.yaml found in upload')
            return

        # Load YAML
        try:
            with open(yaml_path, 'r') as f:
                surface_yaml = yaml.safe_load(f)
        except Exception as e:
            logger.warning(f'SurfaceNormalizer: failed to read surface.yaml: {e}')
            return

        # Create the top-level surface metadata section
        surface_section = section_surface_metadata()

        # Miller indices
        surface_section.surface_miller = surface_yaml.get('surface', {}).get('miller')

        # Sites and their properties
        sites_yaml = surface_yaml.get('sites', [])
        occupations = surface_yaml.get('occupations', {})
        topology = surface_yaml.get('topology', {}).get('neighbours', {})

        for site_yaml in sites_yaml:
            site = section_surface_site()
            site_id = site_yaml.get('id')

            site.site_id = site_id
            site.fractional = site_yaml.get('fractional')
            site.occupation = occupations.get(site_id)
            site.neighbours = topology.get(site_id)

            surface_section.sites.append(site)

        # Attach to archive.data
        if archive.data is None:
            logger.warning('SurfaceNormalizer: archive.data is None, cannot attach metadata')
            return

        archive.data.x_vasp_surface_metadata = surface_section

        logger.info('SurfaceNormalizer: surface metadata successfully added')

