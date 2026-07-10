"""
CareerLens

Phase 2 Pipeline Runner

Executes the complete analytics pipeline.

Author: CareerLens
Python Version: 3.14
"""

from logger import get_logger
from visualization import VisualizationGenerator

from exploratory_analysis import ExploratoryAnalysis
from business_analysis import BusinessAnalysis
from sql_analysis import SQLAnalysis
from kpi_generator import KPIGenerator
from export_powerbi import PowerBIExporter
from report_generator import ReportGenerator

logger = get_logger(__name__)


def main() -> None:

    logger.info("=" * 60)
    logger.info("Starting CareerLens Phase 2")
    logger.info("=" * 60)

    ExploratoryAnalysis().execute()

    BusinessAnalysis().execute()

    SQLAnalysis().execute()

    KPIGenerator().execute()

    PowerBIExporter().execute()
    
    VisualizationGenerator().execute()

    ReportGenerator().execute()

    logger.info("=" * 60)
    logger.info("Phase 2 Completed Successfully")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()