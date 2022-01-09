import sentry_sdk

sentry_sdk.init(
    "https://d2744aa667304febbb8766ca55f650f8@o1086610.ingest.sentry.io/6098931",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)