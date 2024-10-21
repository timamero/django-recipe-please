## Code Refactor

**Description:**
- Briefly describe the purpose and scope of the refactor.

**Changes Made:**
- List the main changes and improvements.
  - Extracted `HelperFunction` from `Component.js` to `utils.js`.
  - Replaced `componentDidMount` with `useEffect` in `NewComponent`.

**Related Issues:**
- Closes #issue-number (if applicable)

**Motivation:**
- Explain why the refactor was necessary.
  - Improve code readability and maintainability.
  - Reduce redundancy in the codebase.

**Testing:**
- Outline any testing performed to ensure no regressions.
  - Unit tests in `RefactoredComponent.test.js` passed.
  - No changes to existing behavior observed.

**Additional Notes:**
- Any known issues or potential follow-ups.
