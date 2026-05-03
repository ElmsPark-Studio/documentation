---
title: "EP Email Quiz"
description: "Adds quiz field types with automatic scoring and grading to EP Email contact forms. Multiple choice, true/false, rating, and configurable grade bands."
sidebar:
  order: 29
---

EP Email Quiz adds quiz field types to [EP Email](/plugins/ep-email/)'s contact forms. Define multiple-choice and true/false questions with correct answers, configure grade bands ("A: 90%+, B: 75%+, ..."), and the plugin auto-scores every submission.

Published by [ElmsPark Studio](https://elmspark.com).

## Use cases

- **Lead qualification quizzes.** "What's your budget? What's your timeline? What do you know about X?" — score the answers, route high-scorers to a call scheduler.
- **Knowledge checks.** Test readers after a tutorial.
- **Assessments.** Simple self-paced tests.
- **Personality quizzes.** Use grade bands as personas ("You're a Planner", "You're a Doer").

## Field types added

- **`quiz_multiple`** — multiple-choice, one correct answer.
- **`quiz_multiple_many`** — multiple-choice, multiple correct answers.
- **`quiz_true_false`** — true/false.
- **`quiz_rating`** — Likert-style rating that contributes to a score.

Each field takes a `correct` option or a `weight` option. Correct answers contribute points; wrong answers don't.

## Grade bands

Configure score-to-grade mapping:

```json
"grade_bands": [
  { "min": 90, "label": "Excellent", "message": "You aced it." },
  { "min": 75, "label": "Good", "message": "Solid understanding." },
  { "min": 50, "label": "Fair", "message": "Some gaps to fill." },
  { "min": 0, "label": "Needs work", "message": "Worth a refresher." }
]
```

The band matching the submission's score is shown on the success page and included in the admin notification.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email** (required)
- **EP Suite base class**

## Installation

1. Install **EP Email** first.
2. Download `ep-email-quiz.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.

## Example form

```json
{
  "form_id": "marketing-knowledge",
  "title": "How much do you know about marketing?",
  "fields": [
    {
      "type": "quiz_multiple",
      "id": "q1",
      "label": "What does CTR stand for?",
      "options": [
        { "value": "a", "label": "Click-through rate" },
        { "value": "b", "label": "Customer transaction record" },
        { "value": "c", "label": "Content testing ratio" }
      ],
      "correct": "a",
      "points": 1
    },
    {
      "type": "quiz_true_false",
      "id": "q2",
      "label": "Meta descriptions directly affect search rankings.",
      "correct": false,
      "points": 1
    }
  ],
  "grade_bands": [
    { "min": 80, "label": "Pro", "message": "You know your stuff." },
    { "min": 40, "label": "Learner", "message": "Getting there." },
    { "min": 0, "label": "Starter", "message": "Want to learn more?" }
  ]
}
```

## The submission view

Admin view of a quiz submission shows:

- Every question with the submitter's answer and whether it was correct.
- Total score and percentage.
- Grade band achieved.
- Time taken (from form open to submit).

Useful for spotting patterns — which questions everyone gets wrong are prime candidates for extra teaching material.

## Per-question feedback

Add a `feedback` option to any question for custom feedback shown on the success page:

```json
{
  "type": "quiz_multiple",
  "id": "q1",
  "correct": "a",
  "feedback": {
    "correct": "Right, CTR means click-through rate.",
    "incorrect": "CTR stands for click-through rate."
  }
}
```

## Troubleshooting

### "Scores come out wrong"

Check `points` is set on each question. Missing `points` defaults to 1 but can be confusing if some questions are weighted differently than you think.

### "Success page shows no grade band"

Grade bands are optional. If you didn't configure them, no band shows — the score alone is recorded.

### "Submitter can see correct answers in page source"

They can. Quiz fields carry correct answers in the form definition, which is rendered to the page. If you need cheating-proof assessments, this plugin isn't the right tool — you need a server-validated exam platform.

### "Multiple correct answers field doesn't score properly"

`quiz_multiple_many` requires `correct` to be an array of values: `"correct": ["a", "c"]`. Full points only if the submitter picked exactly those values.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
