# CVE-2020-25670 (High) detected in linuxlinux-4.19.313

- URL: https://github.com/RenukaSelvar/kernel_smp/issues/408
- Repo: RenukaSelvar/kernel_smp (language: C)
- State: open; created 2024-05-15T18:24:02Z; status ok; passes offcwe

## Issue body

reporter (NONE) · mend-bolt-for-github[bot] · 2024-05-15T18:24:02Z · https://github.com/RenukaSelvar/kernel_smp/issues/408

## CVE-2020-25670 - High Severity Vulnerability
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/vulnerability_details.png' width=19 height=20> Vulnerable Library - <b>linuxlinux-4.19.313</b></summary>
<p>

<p>The Linux Kernel</p>
<p>Library home page: <a href=https://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/?wsslib=linux>https://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/?wsslib=linux</a></p>

<p>Found in base branch: <b>master</b></p></p>
</details>
</p></p>
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/vulnerability_details.png' width=19 height=20> Vulnerable Source Files (1)</summary>
<p></p>
<p>

  <img src='https://s3.amazonaws.com/wss-public/bitbucketImages/xRedImage.png' width=19 height=20> <b>/net/nfc/llcp_sock.c</b>
</p>
</details>
<p></p>
</p>
</details>
<p></p>
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/high_vul.png?' width=19 height=20> Vulnerability Details</summary>
<p>  
  
A vulnerability was found in Linux Kernel where refcount leak in llcp_sock_bind() causing use-after-free which might lead to privilege escalations.

<p>Publish Date: 2021-05-26
<p>URL: <a href=https://www.mend.io/vulnerability-database/CVE-2020-25670>CVE-2020-25670</a></p>
</p>
</details>
<p></p>
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/cvss3.png' width=19 height=20> CVSS 3 Score Details (<b>7.8</b>)</summary>
<p>

Base Score Metrics:
- Exploitability Metrics:
  - Attack Vector: Local
  - Attack Complexity: Low
  - Privileges Required: Low
  - User Interaction: None
  - Scope: Unchanged
- Impact Metrics:
  - Confidentiality Impact: High
  - Integrity Impact: High
  - Availability Impact: High
</p>
For more information on CVSS3 Scores, click <a href="https://www.first.org/cvss/calculator/3.0">here</a>.
</p>
</details>
<p></p>

***
Step up your Open Source Security Game with Mend [here](https://www.whitesourcesoftware.com/full_solution_bolt_github)

## Comment 2179326442

reporter (NONE) · mend-bolt-for-github[bot] · 2024-06-19T19:02:43Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2179326442

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2211845598

reporter (NONE) · mend-bolt-for-github[bot] · 2024-07-06T18:34:40Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2211845598

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2261799166

reporter (NONE) · mend-bolt-for-github[bot] · 2024-08-01T01:57:28Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2261799166

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2271957446

reporter (NONE) · mend-bolt-for-github[bot] · 2024-08-06T19:05:28Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2271957446

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2366916371

reporter (NONE) · mend-bolt-for-github[bot] · 2024-09-22T18:54:23Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2366916371

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2372068974

reporter (NONE) · mend-bolt-for-github[bot] · 2024-09-24T18:57:07Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2372068974

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2521133169

reporter (NONE) · mend-bolt-for-github[bot] · 2024-12-05T18:33:32Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2521133169

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2550110059

reporter (NONE) · mend-bolt-for-github[bot] · 2024-12-18T01:51:39Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2550110059

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2634771255

reporter (NONE) · mend-bolt-for-github[bot] · 2025-02-04T18:38:02Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2634771255

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2646468620

reporter (NONE) · mend-bolt-for-github[bot] · 2025-02-09T18:22:25Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2646468620

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2675268757

reporter (NONE) · mend-bolt-for-github[bot] · 2025-02-21T18:30:26Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2675268757

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2677040722

reporter (NONE) · mend-bolt-for-github[bot] · 2025-02-23T18:30:59Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2677040722

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2711496461

reporter (NONE) · mend-bolt-for-github[bot] · 2025-03-10T18:38:07Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2711496461

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2736670869

reporter (NONE) · mend-bolt-for-github[bot] · 2025-03-19T13:34:19Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2736670869

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2755434204

reporter (NONE) · mend-bolt-for-github[bot] · 2025-03-26T18:42:53Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2755434204

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2759374649

reporter (NONE) · mend-bolt-for-github[bot] · 2025-03-27T20:14:43Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-2759374649

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 3938330602

reporter (NONE) · mend-bolt-for-github[bot] · 2026-02-21T07:08:13Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-3938330602

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 4324584509

reporter (NONE) · mend-bolt-for-github[bot] · 2026-04-27T06:17:56Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-4324584509

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 4427845111

reporter (NONE) · mend-bolt-for-github[bot] · 2026-05-12T06:20:00Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-4427845111

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 5590551559

reporter (NONE) · mend-bolt-for-github[bot] · 2026-09-08T19:20:56Z · https://github.com/RenukaSelvar/kernel_smp/issues/408#issuecomment-5590551559

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.
