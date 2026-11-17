export const meta = {
  name: 'review-branch',
  description: 'Rýnir greinina frá fjórum sjónarhornum og sannreynir hverja athugasemd',
  whenToUse: 'Áður en merge request er opnað á stærri breytingu',
  phases: [
    { title: 'Rýni', detail: 'einn code-reviewer á hvert sjónarhorn' },
    { title: 'Sannreyna', detail: 'reynt að hrekja hverja athugasemd' },
  ],
}

const LENSES = [
  { key: 'api', ask: 'correctness of the FastAPI endpoints and TaskService' },
  { key: 'types', ask: 'whether web/src/api.ts still mirrors api/app/models.py' },
  { key: 'tests', ask: 'missing or weak pytest coverage for the changed behaviour' },
  { key: 'scope', ask: 'changes that go beyond what the branch name and commits say was asked' },
]

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: { file: { type: 'string' }, line: { type: 'number' }, problem: { type: 'string' } },
        required: ['file', 'problem'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT = {
  type: 'object',
  properties: { real: { type: 'boolean' }, why: { type: 'string' } },
  required: ['real', 'why'],
}

// pipeline: each lens verifies its own findings as soon as its review is done
const results = await pipeline(
  LENSES,
  (lens) =>
    agent(`Review \`git diff main...HEAD\` in this repo. Look only at: ${lens.ask}. Report concrete defects, not style.`, {
      label: `rýni:${lens.key}`,
      phase: 'Rýni',
      agentType: 'code-reviewer',
      schema: FINDINGS,
    }),
  (review) =>
    parallel(
      review.findings.map((f) => () =>
        agent(`Try to refute this review finding by reading the code. ${f.file}:${f.line ?? '?'} ${f.problem}`, {
          label: `sannreyna:${f.file}`,
          phase: 'Sannreyna',
          schema: VERDICT,
        }).then((v) => ({ ...f, ...v })),
      ),
    ),
)

return results.flat().filter(Boolean).filter((f) => f.real)
