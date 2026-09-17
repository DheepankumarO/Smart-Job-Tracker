CREATE TABLE IF NOT EXISTS applications (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    company VARCHAR(150) NOT NULL,
    position VARCHAR(150) NOT NULL,
    location VARCHAR(150) NOT NULL,
    job_url TEXT,
    application_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Saved',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_application_status
        CHECK (
            status IN (
                'Saved',
                'Applied',
                'Interview',
                'Offer',
                'Rejected',
                'Withdrawn'
            )
        )
);