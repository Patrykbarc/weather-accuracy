"""add forecast_error view

Revision ID: 5ad24097d703
Revises: 9fc6a2000b44
Create Date: 2026-08-12 20:29:55.715731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '5ad24097d703'
down_revision: Union[str, Sequence[str], None] = '9fc6a2000b44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE VIEW forecast_error AS
    SELECT
	    f.location_id,
	    f.target_date,
	    f.fetched_at,
	    CAST(julianday(f.target_date) - julianday(f.fetched_at) AS INTEGER) AS lead_time,
	    ROUND(f.temp_max -		o.temp_max,		 2) AS temp_max_error,
	    ROUND(f.temp_min - 		o.temp_min,		 2) AS temp_min_error,
	    ROUND(f.wind_gusts -	o.wind_gusts,	 2) AS wind_gusts_error,
	    ROUND(f.precipitation - o.precipitation, 2) AS precipitation_error
    FROM forecast f
    JOIN observation o 
	    ON o.location_id = f.location_id
	    AND o.measured_at = f.target_date
    """)
    pass


def downgrade() -> None:
    op.execute("DROP VIEW forecast_error")
    pass
