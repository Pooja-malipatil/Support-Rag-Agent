# Each entry has:
# question     — what the user asks
# answer_contains — keywords the correct answer must contain
# expected_chunks — chunk IDs that should appear in top 5 retrieval
# should_refuse   — True if system must say "I don't know"
# question_type   — for grouping results in the report

GOLDEN_DATASET = [
    # --- Type 1: Direct lookup ---
    {
        "question": "How many API keys can free accounts have?",
        "answer_contains": ["3", "three"],
        "expected_chunks": ["api-keys-faq-chunk-2"],
        "should_refuse": False,
        "question_type": "direct_lookup",
    },
    {
        "question": "What HTTP status code is returned when rate limit is exceeded?",
        "answer_contains": ["429"],
        "expected_chunks": ["api-usage-policy-chunk-0"],
        "should_refuse": False,
        "question_type": "direct_lookup",
    },
    {
        "question": "Where do I go to generate a new API key?",
        "answer_contains": ["settings", "api keys"],
        "expected_chunks": ["api-keys-faq-chunk-0"],
        "should_refuse": False,
        "question_type": "direct_lookup",
    },
    {
        "question": "What should I do immediately if my API key is leaked?",
        "answer_contains": ["revoke"],
        "expected_chunks": ["api-keys-faq-chunk-3"],
        "should_refuse": False,
        "question_type": "direct_lookup",
    },

    # --- Type 2: Multi-doc ---
    {
        "question": "How do I generate and then securely store my API key?",
        "answer_contains": ["settings", "environment"],
        "expected_chunks": [
            "api-keys-faq-chunk-0",
            "authentication-setup-guide-chunk-2"
        ],
        "should_refuse": False,
        "question_type": "multi_doc",
    },
    {
        "question": "What are the steps to rotate a key in production safely?",
        "answer_contains": ["generate", "revoke", "deploy"],
        "expected_chunks": [
            "authentication-setup-guide-chunk-4",
            "api-keys-faq-chunk-1"
        ],
        "should_refuse": False,
        "question_type": "multi_doc",
    },

    # --- Type 3: Tricky/requires inference ---
    {
        "question": "Can I hardcode my API key in my JavaScript frontend?",
        "answer_contains": ["restricted", "limited", "client-side", "not"],
        "expected_chunks": ["api-usage-policy-chunk-1"],
        "should_refuse": False,
        "question_type": "tricky",
    },
    {
        "question": "How do I authenticate my first API request?",
        "answer_contains": ["bearer", "authorization", "header"],
        "expected_chunks": ["authentication-setup-guide-chunk-3"],
        "should_refuse": False,
        "question_type": "tricky",
    },
    {
        "question": "What happens to my old key when I generate a new one?",
        "answer_contains": ["revoke", "still works", "replace"],
        "expected_chunks": ["api-keys-faq-chunk-1"],
        "should_refuse": False,
        "question_type": "tricky",
    },

    # --- Type 4: Must refuse ---
    {
        "question": "What is the refund policy?",
        "answer_contains": [],
        "expected_chunks": [],
        "should_refuse": True,
        "question_type": "unanswerable",
    },
    {
        "question": "How do I contact customer support by phone?",
        "answer_contains": [],
        "expected_chunks": [],
        "should_refuse": True,
        "question_type": "unanswerable",
    },
    {
        "question": "What programming languages does the SDK support?",
        "answer_contains": [],
        "expected_chunks": [],
        "should_refuse": True,
        "question_type": "unanswerable",
    },
    {
        "question": "How much does the Pro plan cost per month?",
        "answer_contains": [],
        "expected_chunks": [],
        "should_refuse": True,
        "question_type": "unanswerable",
    },
]