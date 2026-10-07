# CVE-2020-25671 (High) detected in linuxlinux-4.19.313

- URL: https://github.com/RenukaSelvar/kernel_smp/issues/407
- Repo: RenukaSelvar/kernel_smp (language: C)
- State: open; created 2024-05-15T18:24:00Z; status ok; passes offcwe

## Issue body

reporter (NONE) · mend-bolt-for-github[bot] · 2024-05-15T18:24:00Z · https://github.com/RenukaSelvar/kernel_smp/issues/407

## CVE-2020-25671 - High Severity Vulnerability
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
  
A vulnerability was found in Linux Kernel, where a refcount leak in llcp_sock_connect() causing use-after-free which might lead to privilege escalations.

<p>Publish Date: 2021-05-26
<p>URL: <a href=https://www.mend.io/vulnerability-database/CVE-2020-25671>CVE-2020-25671</a></p>
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

## Comment 2179326328

reporter (NONE) · mend-bolt-for-github[bot] · 2024-06-19T19:02:39Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2179326328

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2211845510

reporter (NONE) · mend-bolt-for-github[bot] · 2024-07-06T18:34:36Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2211845510

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2261799061

reporter (NONE) · mend-bolt-for-github[bot] · 2024-08-01T01:57:24Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2261799061

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2271957309

reporter (NONE) · mend-bolt-for-github[bot] · 2024-08-06T19:05:24Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2271957309

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2366916356

reporter (NONE) · mend-bolt-for-github[bot] · 2024-09-22T18:54:19Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2366916356

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2372068901

reporter (NONE) · mend-bolt-for-github[bot] · 2024-09-24T18:57:05Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2372068901

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2521133050

reporter (NONE) · mend-bolt-for-github[bot] · 2024-12-05T18:33:27Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2521133050

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2550109990

reporter (NONE) · mend-bolt-for-github[bot] · 2024-12-18T01:51:37Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2550109990

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2634771133

reporter (NONE) · mend-bolt-for-github[bot] · 2025-02-04T18:37:58Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2634771133

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2646468598

reporter (NONE) · mend-bolt-for-github[bot] · 2025-02-09T18:22:23Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2646468598

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2675268576

reporter (NONE) · mend-bolt-for-github[bot] · 2025-02-21T18:30:21Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2675268576

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2677040703

reporter (NONE) · mend-bolt-for-github[bot] · 2025-02-23T18:30:57Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2677040703

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2711496002

reporter (NONE) · mend-bolt-for-github[bot] · 2025-03-10T18:38:02Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2711496002

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2736670711

reporter (NONE) · mend-bolt-for-github[bot] · 2025-03-19T13:34:16Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2736670711

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 2755434035

reporter (NONE) · mend-bolt-for-github[bot] · 2025-03-26T18:42:48Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2755434035

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 2759374572

reporter (NONE) · mend-bolt-for-github[bot] · 2025-03-27T20:14:41Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-2759374572

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 3938330515

reporter (NONE) · mend-bolt-for-github[bot] · 2026-02-21T07:08:09Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-3938330515

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 4324584069

reporter (NONE) · mend-bolt-for-github[bot] · 2026-04-27T06:17:51Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-4324584069

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 4427844578

reporter (NONE) · mend-bolt-for-github[bot] · 2026-05-12T06:19:55Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-4427844578

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 5590551001

reporter (NONE) · mend-bolt-for-github[bot] · 2026-09-08T19:20:53Z · https://github.com/RenukaSelvar/kernel_smp/issues/407#issuecomment-5590551001

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.
