# GitHub Workflows

This directory contains GitHub Actions workflows for the Multi-Region Microservice on AWS project.

## Dependency Vulnerability Scanning

The `dependency-vulnerability-scan.yml` workflow scans all project dependencies for known security vulnerabilities and generates comprehensive reports.

### Features

- **Comprehensive Coverage**: Scans Java, Node.js, and Go codebases
- **Multiple Scanning Tools**:
  - Java: OWASP Dependency Check and Trivy
  - Node.js: npm audit and Trivy
  - Go: govulncheck and Trivy
- **Automated Reporting**: Generates consolidated reports and uploads detailed scan results as artifacts
- **GitHub Security Integration**: Uploads SARIF reports to GitHub Security tab
- **GitHub Pages Integration**: Publishes summary reports to GitHub Pages (when run on main/master branch)

### Workflow Triggers

The workflow runs:
- On a weekly schedule (midnight every Sunday)
- On push to main/master branches
- On pull requests to main/master branches
- Manually via workflow_dispatch

### Viewing Reports

After the workflow runs, you can access the reports in several ways:

1. **GitHub Security Tab**: Critical and high vulnerabilities are displayed in the repository's Security tab
2. **Workflow Artifacts**: Detailed reports are available as workflow artifacts for 7-30 days
3. **GitHub Pages**: A consolidated summary report is published to GitHub Pages (when run on main/master branch)

### Manual Execution

To run the vulnerability scan manually:

1. Go to the "Actions" tab in your GitHub repository
2. Select the "Dependency Vulnerability Scan" workflow
3. Click "Run workflow"
4. Select the branch to scan
5. Click "Run workflow"

### Customization

You can customize the workflow by editing the `.github/workflows/dependency-vulnerability-scan.yml` file:

- Adjust the schedule by modifying the `cron` expression
- Change the severity levels for Trivy scans
- Add or remove services from the matrix
- Modify the report generation script

Note: The workflow uses Python 3.11 and specific versions of actions for stability.

### Interpreting Results

The workflow generates several types of reports:

- **OWASP Dependency Check Reports**: HTML reports with detailed information about Java vulnerabilities
- **npm audit Reports**: JSON reports with Node.js package vulnerabilities
- **Trivy Reports**: SARIF reports with filesystem vulnerabilities
- **Consolidated Summary**: Markdown report with links to detailed reports and recommendations

### Troubleshooting

If the workflow fails:

1. Check the workflow logs for error messages
2. Ensure all required secrets are configured
3. Verify that the repository structure matches the paths in the workflow
4. Check if any of the scanning tools are having issues or rate limiting