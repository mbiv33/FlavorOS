CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS client_accounts (
    client_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    default_authority_mode TEXT NOT NULL DEFAULT 'draft_only',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS provider_connections (
    provider_connection_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL REFERENCES client_accounts(client_id) ON DELETE CASCADE,
    provider TEXT NOT NULL,
    account_alias TEXT NOT NULL,
    connection_status TEXT NOT NULL DEFAULT 'pending',
    last_sync_at TIMESTAMPTZ,
    last_error_at TIMESTAMPTZ,
    last_error_summary TEXT,
    capabilities_json JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (client_id, provider, account_alias)
);

CREATE TABLE IF NOT EXISTS oauth_accounts (
    oauth_account_id TEXT PRIMARY KEY,
    provider_connection_id TEXT NOT NULL REFERENCES provider_connections(provider_connection_id) ON DELETE CASCADE,
    scopes_json JSONB NOT NULL DEFAULT '[]'::JSONB,
    token_expires_at TIMESTAMPTZ,
    refresh_status TEXT NOT NULL DEFAULT 'unknown',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS provider_events (
    provider_event_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL REFERENCES client_accounts(client_id) ON DELETE CASCADE,
    provider_connection_id TEXT NOT NULL REFERENCES provider_connections(provider_connection_id) ON DELETE CASCADE,
    provider TEXT NOT NULL,
    external_object_id TEXT NOT NULL,
    external_thread_id TEXT,
    event_type TEXT NOT NULL,
    occurred_at TIMESTAMPTZ,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    payload_json JSONB NOT NULL DEFAULT '{}'::JSONB,
    payload_text_preview TEXT,
    dedupe_key TEXT NOT NULL,
    processing_status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (provider_connection_id, dedupe_key)
);

CREATE INDEX IF NOT EXISTS idx_provider_events_client_provider
    ON provider_events (client_id, provider, ingested_at DESC);

CREATE TABLE IF NOT EXISTS sync_checkpoints (
    sync_checkpoint_id TEXT PRIMARY KEY,
    provider_connection_id TEXT NOT NULL REFERENCES provider_connections(provider_connection_id) ON DELETE CASCADE,
    checkpoint_type TEXT NOT NULL,
    checkpoint_value TEXT NOT NULL,
    checkpoint_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (provider_connection_id, checkpoint_type)
);

CREATE TABLE IF NOT EXISTS normalized_threads (
    normalized_thread_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL REFERENCES client_accounts(client_id) ON DELETE CASCADE,
    thread_kind TEXT NOT NULL,
    provider TEXT NOT NULL,
    external_thread_id TEXT,
    title TEXT,
    primary_counterparty TEXT,
    thread_status TEXT NOT NULL DEFAULT 'active',
    latest_provider_event_id TEXT REFERENCES provider_events(provider_event_id) ON DELETE SET NULL,
    last_activity_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_normalized_threads_client_activity
    ON normalized_threads (client_id, last_activity_at DESC);

CREATE TABLE IF NOT EXISTS normalized_items (
    normalized_item_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL REFERENCES client_accounts(client_id) ON DELETE CASCADE,
    normalized_thread_id TEXT REFERENCES normalized_threads(normalized_thread_id) ON DELETE SET NULL,
    provider_event_id TEXT NOT NULL REFERENCES provider_events(provider_event_id) ON DELETE CASCADE,
    provider TEXT NOT NULL,
    item_type TEXT NOT NULL,
    direction TEXT NOT NULL,
    received_at TIMESTAMPTZ,
    from_entities_json JSONB NOT NULL DEFAULT '[]'::JSONB,
    to_entities_json JSONB NOT NULL DEFAULT '[]'::JSONB,
    subject TEXT,
    body_markdown TEXT,
    requires_response BOOLEAN NOT NULL DEFAULT FALSE,
    requires_approval BOOLEAN NOT NULL DEFAULT FALSE,
    suggested_route TEXT,
    origin_action_type TEXT,
    origin_write_target_json JSONB NOT NULL DEFAULT '{}'::JSONB,
    normalization_version TEXT NOT NULL DEFAULT 'v1',
    classification_json JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_normalized_items_client_received
    ON normalized_items (client_id, received_at DESC);

CREATE TABLE IF NOT EXISTS work_orders (
    work_order_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL REFERENCES client_accounts(client_id) ON DELETE CASCADE,
    normalized_item_id TEXT REFERENCES normalized_items(normalized_item_id) ON DELETE SET NULL,
    source_agent TEXT NOT NULL,
    target_agent TEXT NOT NULL,
    task_type TEXT NOT NULL,
    priority TEXT NOT NULL DEFAULT 'P1',
    status TEXT NOT NULL DEFAULT 'queued',
    deliverable_type TEXT NOT NULL,
    requires_approval BOOLEAN NOT NULL DEFAULT FALSE,
    artifact_target_path TEXT,
    input_json JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_work_orders_target_status
    ON work_orders (target_agent, status, created_at DESC);

CREATE TABLE IF NOT EXISTS agent_reports (
    agent_report_id TEXT PRIMARY KEY,
    work_order_id TEXT NOT NULL REFERENCES work_orders(work_order_id) ON DELETE CASCADE,
    agent TEXT NOT NULL,
    status TEXT NOT NULL,
    summary TEXT NOT NULL,
    user_facing_response TEXT,
    vault_file TEXT,
    requires_approval BOOLEAN NOT NULL DEFAULT FALSE,
    report_json JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_reports_work_order
    ON agent_reports (work_order_id, created_at DESC);

CREATE TABLE IF NOT EXISTS artifacts (
    artifact_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL REFERENCES client_accounts(client_id) ON DELETE CASCADE,
    artifact_type TEXT NOT NULL,
    source_work_order_id TEXT REFERENCES work_orders(work_order_id) ON DELETE SET NULL,
    source_report_id TEXT REFERENCES agent_reports(agent_report_id) ON DELETE SET NULL,
    vault_path TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft',
    rendered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    related_provider_event_id TEXT REFERENCES provider_events(provider_event_id) ON DELETE SET NULL,
    related_normalized_item_id TEXT REFERENCES normalized_items(normalized_item_id) ON DELETE SET NULL,
    metadata_json JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_artifacts_client_rendered
    ON artifacts (client_id, rendered_at DESC);

CREATE TABLE IF NOT EXISTS approval_decisions (
    approval_decision_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL REFERENCES client_accounts(client_id) ON DELETE CASCADE,
    artifact_id TEXT REFERENCES artifacts(artifact_id) ON DELETE SET NULL,
    work_order_id TEXT REFERENCES work_orders(work_order_id) ON DELETE SET NULL,
    decision_owner TEXT NOT NULL,
    decision_state TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    exact_side_effect TEXT NOT NULL,
    decision_notes TEXT,
    decided_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata_json JSONB NOT NULL DEFAULT '{}'::JSONB
);

CREATE TABLE IF NOT EXISTS outbound_actions (
    outbound_action_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL REFERENCES client_accounts(client_id) ON DELETE CASCADE,
    normalized_item_id TEXT REFERENCES normalized_items(normalized_item_id) ON DELETE SET NULL,
    artifact_id TEXT REFERENCES artifacts(artifact_id) ON DELETE SET NULL,
    provider TEXT NOT NULL,
    action_type TEXT NOT NULL,
    target_reference_json JSONB NOT NULL DEFAULT '{}'::JSONB,
    payload_json JSONB NOT NULL DEFAULT '{}'::JSONB,
    approval_decision_id TEXT REFERENCES approval_decisions(approval_decision_id) ON DELETE SET NULL,
    status TEXT NOT NULL DEFAULT 'staged',
    attempt_count INTEGER NOT NULL DEFAULT 0,
    last_attempt_at TIMESTAMPTZ,
    last_error_summary TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_outbound_actions_status
    ON outbound_actions (provider, status, created_at DESC);

CREATE TABLE IF NOT EXISTS sync_receipts (
    sync_receipt_id TEXT PRIMARY KEY,
    outbound_action_id TEXT NOT NULL REFERENCES outbound_actions(outbound_action_id) ON DELETE CASCADE,
    provider TEXT NOT NULL,
    external_result_id TEXT,
    receipt_status TEXT NOT NULL,
    response_code TEXT,
    response_summary TEXT,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    payload_json JSONB NOT NULL DEFAULT '{}'::JSONB
);

INSERT INTO client_accounts (client_id, display_name, status, default_authority_mode)
VALUES ('marcus', 'Marcus', 'active', 'draft_only')
ON CONFLICT (client_id) DO NOTHING;

INSERT INTO provider_connections (
    provider_connection_id,
    client_id,
    provider,
    account_alias,
    connection_status,
    capabilities_json
)
VALUES
    ('conn-marcus-gmail', 'marcus', 'gmail', 'marcus_primary', 'healthy', '{"ingest":true,"draft":true,"send":false}'::JSONB),
    ('conn-marcus-calendar', 'marcus', 'google_calendar', 'marcus_primary', 'healthy', '{"ingest":true,"propose":true,"commit":false}'::JSONB),
    ('conn-marcus-whatsapp', 'marcus', 'whatsapp', 'marcus_phone', 'syncing', '{"ingest":true,"reply":false}'::JSONB),
    ('conn-marcus-social', 'marcus', 'social_dm', 'marcus_social', 'review_mode', '{"ingest":true,"reply":false}'::JSONB)
ON CONFLICT (provider_connection_id) DO NOTHING;
