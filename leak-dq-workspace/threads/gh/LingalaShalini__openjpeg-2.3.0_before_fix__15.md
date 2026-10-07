# CVE-2019-6988 (Medium) detected in openjpegv2.3.0

- URL: https://github.com/LingalaShalini/openjpeg-2.3.0_before_fix/issues/15
- Repo: LingalaShalini/openjpeg-2.3.0_before_fix (language: C)
- State: open; created 2021-08-02T06:51:41Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · mend-bolt-for-github[bot] · 2021-08-02T06:51:41Z · https://github.com/LingalaShalini/openjpeg-2.3.0_before_fix/issues/15

## CVE-2019-6988 - Medium Severity Vulnerability
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/vulnerability_details.png' width=19 height=20> Vulnerable Library - <b>openjpegv2.3.0</b></summary>
<p>

<p>Official repository of the OpenJPEG project</p>
<p>Library home page: <a href=https://github.com/uclouvain/openjpeg.git>https://github.com/uclouvain/openjpeg.git</a></p>
<p>Found in HEAD commit: <a href="https://github.com/LingalaShalini/openjpeg-2.3.0_before_fix/commit/3501163dd1d68645efcce586f29683574a46c95f">3501163dd1d68645efcce586f29683574a46c95f</a></p>

<p>Found in base branch: <b>master</b></p></p>
</details>
</p></p>
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/vulnerability_details.png' width=19 height=20> Vulnerable Source Files (1)</summary>
<p></p>
<p>

  <img src='https://s3.amazonaws.com/wss-public/bitbucketImages/xRedImage.png' width=19 height=20> <b>/src/bin/jp2/convertbmp.c</b>
</p>
</details>
<p></p>
</p>
</details>
<p></p>
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/medium_vul.png?' width=19 height=20> Vulnerability Details</summary>
<p>  
  
An issue was discovered in OpenJPEG 2.3.0. It allows remote attackers to cause a denial of service (attempted excessive memory allocation) in opj_calloc in openjp2/opj_malloc.c, when called from opj_tcd_init_tile in openjp2/tcd.c, as demonstrated by the 64-bit opj_decompress.

<p>Publish Date: 2019-01-28
<p>URL: <a href=https://www.mend.io/vulnerability-database/CVE-2019-6988>CVE-2019-6988</a></p>
</p>
</details>
<p></p>
<details><summary><img src='https://whitesource-resources.whitesourcesoftware.com/cvss3.png' width=19 height=20> CVSS 3 Score Details (<b>6.5</b>)</summary>
<p>

Base Score Metrics:
- Exploitability Metrics:
  - Attack Vector: Network
  - Attack Complexity: Low
  - Privileges Required: None
  - User Interaction: Required
  - Scope: Unchanged
- Impact Metrics:
  - Confidentiality Impact: None
  - Integrity Impact: None
  - Availability Impact: High
</p>
For more information on CVSS3 Scores, click <a href="https://www.first.org/cvss/calculator/3.0">here</a>.
</p>
</details>
<p></p>

***
Step up your Open Source Security Game with Mend [here](https://www.whitesourcesoftware.com/full_solution_bolt_github)

## Comment 1218828665

reporter (CONTRIBUTOR) · mend-bolt-for-github[bot] · 2022-08-18T01:04:58Z · https://github.com/LingalaShalini/openjpeg-2.3.0_before_fix/issues/15#issuecomment-1218828665

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 1288264989

reporter (CONTRIBUTOR) · mend-bolt-for-github[bot] · 2022-10-24T01:02:22Z · https://github.com/LingalaShalini/openjpeg-2.3.0_before_fix/issues/15#issuecomment-1288264989

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.

## Comment 4062333666

reporter (CONTRIBUTOR) · mend-bolt-for-github[bot] · 2026-03-15T06:04:25Z · https://github.com/LingalaShalini/openjpeg-2.3.0_before_fix/issues/15#issuecomment-4062333666

:heavy_check_mark: This issue was automatically closed by Mend because the vulnerable library in the specific branch(es) was either marked as ignored or it is no longer part of the Mend inventory.

## Comment 4900654720

reporter (CONTRIBUTOR) · mend-bolt-for-github[bot] · 2026-07-07T06:01:46Z · https://github.com/LingalaShalini/openjpeg-2.3.0_before_fix/issues/15#issuecomment-4900654720

:information_source: This issue was automatically re-opened by Mend because the vulnerable library in the specific branch(es) has been detected in the Mend inventory.
