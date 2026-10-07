# CVE-2020-13757 (High) detected in rsa-3.4.2-py2.py3-none-any.whl

- URL: https://github.com/LevyForchh/yugabyte-db/issues/30
- Repo: LevyForchh/yugabyte-db (language: C)
- State: open; created 2021-02-19T01:24:26Z; status ok; passes main

## Issue body

reporter (NONE) · mend-for-github-com[bot] · 2021-02-19T01:24:26Z · https://github.com/LevyForchh/yugabyte-db/issues/30

## CVE-2020-13757 - High Severity Vulnerability
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/vulnerability_details.png' width=19 height=20> Vulnerable Library - <b>rsa-3.4.2-py2.py3-none-any.whl</b></p></summary>

<p>Pure-Python RSA implementation</p>
<p>Library home page: <a href="https://files.pythonhosted.org/packages/e1/ae/baedc9cb175552e95f3395c43055a6a5e125ae4d48a1d7a924baca83e92e/rsa-3.4.2-py2.py3-none-any.whl">https://files.pythonhosted.org/packages/e1/ae/baedc9cb175552e95f3395c43055a6a5e125ae4d48a1d7a924baca83e92e/rsa-3.4.2-py2.py3-none-any.whl</a></p>
<p>Path to dependency file: yugabyte-db/managed/devops/python3_requirements.txt</p>
<p>Path to vulnerable library: yugabyte-db/managed/devops/python3_requirements.txt,yugabyte-db/managed/devops/python_requirements.txt,yugabyte-db/cloud/kubernetes/yb-multiregion-k8s</p>
<p>

Dependency Hierarchy:
  - oauth2client-3.0.0.tar.gz (Root Library)
    - :x: **rsa-3.4.2-py2.py3-none-any.whl** (Vulnerable Library)
<p>Found in HEAD commit: <a href="https://github.com/LevyForchh/yugabyte-db/commit/d5a0ed9bff63893a5435e09333d22846f6bb3acc">d5a0ed9bff63893a5435e09333d22846f6bb3acc</a></p>
<p>Found in base branch: <b>master</b></p>
</p>
</details>
<p></p>
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/high_vul.png' width=19 height=20> Vulnerability Details</summary>
<p>  
  
Python-RSA before 4.1 ignores leading '\0' bytes during decryption of ciphertext. This could conceivably have a security-relevant impact, e.g., by helping an attacker to infer that an application uses Python-RSA, or if the length of accepted ciphertext affects application behavior (such as by causing excessive memory allocation).

<p>Publish Date: 2020-06-01
<p>URL: <a href=https://vuln.whitesourcesoftware.com/vulnerability/CVE-2020-13757>CVE-2020-13757</a></p>
</p>
</details>
<p></p>
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/cvss3.png' width=19 height=20> CVSS 3 Score Details (<b>7.5</b>)</summary>
<p>

Base Score Metrics:
- Exploitability Metrics:
  - Attack Vector: Network
  - Attack Complexity: Low
  - Privileges Required: None
  - User Interaction: None
  - Scope: Unchanged
- Impact Metrics:
  - Confidentiality Impact: High
  - Integrity Impact: None
  - Availability Impact: None
</p>
For more information on CVSS3 Scores, click <a href="https://www.first.org/cvss/calculator/3.0">here</a>.
</p>
</details>
<p></p>
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/suggested_fix.png' width=19 height=20> Suggested Fix</summary>
<p>

<p>Type: Upgrade version</p>
<p>Origin: <a href="https://github.com/sybrenstuvel/python-rsa/commit/3283b1284475cf6c79a7329aee8bd7443cc72672">https://github.com/sybrenstuvel/python-rsa/commit/3283b1284475cf6c79a7329aee8bd7443cc72672</a></p>
<p>Release Date: 2020-06-01</p>
<p>Fix Resolution: rsa - 4.1</p>

</p>
</details>
<p></p>

<!-- <REMEDIATE>{"isOpenPROnVulnerability":false,"isPackageBased":true,"isDefaultBranch":true,"packages":[{"packageType":"Python","packageName":"rsa","packageVersion":"3.4.2","packageFilePaths":["/managed/devops/python3_requirements.txt","/managed/devops/python_requirements.txt","/cloud/kubernetes/yb-multiregion-k8s"],"isTransitiveDependency":true,"dependencyTree":"oauth2client:3.0.0;rsa:3.4.2","isMinimumFixVersionAvailable":true,"minimumFixVersion":"rsa - 4.1"}],"baseBranches":["master"],"vulnerabilityIdentifier":"CVE-2020-13757","vulnerabilityDetails":"Python-RSA before 4.1 ignores leading \u0027\\0\u0027 bytes during decryption of ciphertext. This could conceivably have a security-relevant impact, e.g., by helping an attacker to infer that an application uses Python-RSA, or if the length of accepted ciphertext affects application behavior (such as by causing excessive memory allocation).","vulnerabilityUrl":"https://vuln.whitesourcesoftware.com/vulnerability/CVE-2020-13757","cvss3Severity":"high","cvss3Score":"7.5","cvss3Metrics":{"A":"None","AC":"Low","PR":"None","S":"Unchanged","C":"High","UI":"None","AV":"Network","I":"None"},"extraData":{}}</REMEDIATE> -->
