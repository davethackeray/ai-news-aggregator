"""initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2025-01-20 11:07:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create stories table
    op.create_table('stories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('interesting_score', sa.Float(), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('used_in_email', sa.Boolean(), default=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stories_id'), 'stories', ['id'], unique=False)

    # Create story_metrics table
    op.create_table('story_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('story_id', sa.Integer(), nullable=True),
        sa.Column('email_opens', sa.Integer(), default=0),
        sa.Column('link_clicks', sa.Integer(), default=0),
        sa.Column('time_spent', sa.Float(), nullable=True),
        sa.Column('feedback_score', sa.Float(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_story_metrics_id'), 'story_metrics', ['id'], unique=False)

def downgrade():
    # Drop tables in reverse order
    op.drop_index(op.f('ix_story_metrics_id'), table_name='story_metrics')
    op.drop_table('story_metrics')
    op.drop_index(op.f('ix_stories_id'), table_name='stories')
    op.drop_table('stories')