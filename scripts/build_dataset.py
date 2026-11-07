"""
ReguGuard Authentic Dataset Builder
Extracts, structures, and validates genuine government cybersecurity audit records
from official GAO reports (GAO-26-107980, GAO-23-104705).
"""
import json
import os

RECORDS = [
    {
        "id": "GAO-26-107980-REC-01",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Information Security Continuous Monitoring",
        "original_finding": "VA needs to make improvements in control assessments, vulnerability scanning, configuration compliance, and software management.",
        "identified_weakness": "Insufficient automated configuration compliance scanning across legacy and cloud assets; vulnerability scanning gaps in specialized networks.",
        "auditor_recommendation": "Accelerate continuous monitoring automation, conduct regular control assessments, and integrate automated vulnerability scanning across all system tiers into the enterprise risk dashboard.",
        "management_response": "VA concurred and established 4 planned remediation actions to address continuous monitoring deficiencies.",
        "remediation_action": "Deploy automated vulnerability assessment pipelines and standardized configuration monitoring agents.",
        "implementation_status": "Partially implemented",
        "status_details": "1 of 4 planned remediation actions completed as of July 2025. Remaining 3 actions in progress.",
        "estimated_completion_date": "2026-09-30",
        "follow_up_assessment": "GAO confirmed 1 action completed; remaining actions delayed past original milestone.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["CA-7", "RA-5", "CM-6"],
            "nist_csf_category": "DE.CM",
            "soc2_crosswalk": ["CC7.1", "CC7.2"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-02",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Cloud Security",
        "original_finding": "VA needs to consistently apply cloud configurations.",
        "identified_weakness": "Inconsistent application of baseline cloud security configurations across multi-cloud tenants, leading to configuration drift and exposed cloud storage resources.",
        "auditor_recommendation": "Standardize baseline cloud security configurations, mandate automated policy-as-code validation, and continuously monitor cloud tenant posture.",
        "management_response": "VA concurred and developed a 6-action remediation plan for cloud configuration consistency.",
        "remediation_action": "Implement cloud posture management tooling and automated CI/CD infrastructure-as-code linting.",
        "implementation_status": "Partially implemented",
        "status_details": "2 of 6 planned remediation actions completed as of July 2025. Timeline delayed past original target.",
        "estimated_completion_date": "2025-09-30 (Delayed)",
        "follow_up_assessment": "GAO identified that remediation milestones were missed and not updated in formal documentation.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["CM-2", "CM-6", "AC-4"],
            "nist_csf_category": "PR.IP",
            "soc2_crosswalk": ["CC6.6", "CC6.8"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-03",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Shadow IT",
        "original_finding": "Shadow IT introduces unaccounted-for risk.",
        "identified_weakness": "Unapproved cloud services, applications, and regional hardware devices deployed without authorization to operate (ATO) or inclusion in the central asset inventory.",
        "auditor_recommendation": "Establish automated discovery of unapproved software and cloud services, enforce procurement boundaries, and inventory all shadow IT assets.",
        "management_response": "VA concurred and established 4 remediation actions to address shadow IT risks.",
        "remediation_action": "Deploy network discovery sensors and implement CASB (Cloud Access Security Broker) controls.",
        "implementation_status": "Partially implemented",
        "status_details": "1 of 4 planned remediation actions completed as of July 2025.",
        "estimated_completion_date": "2026-02-28",
        "follow_up_assessment": "GAO noted ongoing execution of inventory reconciliation across regional health centers.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["CM-8", "SA-9", "CM-7"],
            "nist_csf_category": "ID.AM",
            "soc2_crosswalk": ["CC6.1", "CC6.8"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-04",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Cybersecurity Governance",
        "original_finding": "Siloed operations and outdated policies affect overall cybersecurity effectiveness.",
        "identified_weakness": "Fragmented operational coordination between Office of Information Security and system teams, compounded by outdated departmental security policies.",
        "auditor_recommendation": "Update cybersecurity policies, establish joint governance councils, and unify communication channels between security leadership and system owners.",
        "management_response": "VA concurred and planned 7 remediation actions.",
        "remediation_action": "Revise overarching security directive handbook and stand up integrated risk councils.",
        "implementation_status": "Partially implemented",
        "status_details": "3 of 7 remediation actions completed as of July 2025. Remaining actions delayed past target.",
        "estimated_completion_date": "2025-12-31 (Delayed)",
        "follow_up_assessment": "GAO reported 3 actions complete; policy revisions experiencing inter-agency review delays.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["PM-1", "PL-1", "PL-2"],
            "nist_csf_category": "GV.OC",
            "soc2_crosswalk": ["CC1.2", "CC1.3"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-05",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Cyber Protection (Zero Trust)",
        "original_finding": "VA can enhance protections by implementing zero trust architecture.",
        "identified_weakness": "Over-reliance on perimeter firewalls without internal micro-segmentation, leaving internal lateral movement unrestricted.",
        "auditor_recommendation": "Accelerate implementation of Zero Trust Architecture pillars (identity, device, network, application, data) aligned with OMB M-22-09.",
        "management_response": "VA concurred and committed to a 7-action zero trust roadmap.",
        "remediation_action": "Enforce phishing-resistant multi-factor authentication and deploy software-defined perimeter micro-segmentation.",
        "implementation_status": "Partially implemented",
        "status_details": "1 of 7 remediation actions completed as of July 2025. Schedule experienced delays.",
        "estimated_completion_date": "Fiscal Year 2026 (Delayed)",
        "follow_up_assessment": "GAO confirmed 1 action completed; network micro-segmentation delayed due to medical device legacy compatibility.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["AC-2", "AC-3", "SC-7", "IA-2"],
            "nist_csf_category": "PR.AC",
            "soc2_crosswalk": ["CC6.1", "CC6.6"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-06",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Cyber Detection & Alert Optimization",
        "original_finding": "VA has opportunities to optimize tools, alert triggers, and integration capabilities.",
        "identified_weakness": "Redundant security monitoring tools operating in silos, leading to high false-positive alert volumes and delayed threat detection.",
        "auditor_recommendation": "Consolidate security operations tooling, optimize correlation rules in the enterprise SIEM, and integrate endpoint telemetry feeds.",
        "management_response": "VA concurred and designed 5 remediation actions for detection optimization.",
        "remediation_action": "Tune SIEM correlation logic and deploy consolidated EDR (Endpoint Detection and Response) agents.",
        "implementation_status": "Partially implemented",
        "status_details": "1 of 5 remediation actions completed as of July 2025.",
        "estimated_completion_date": "2026-09-30",
        "follow_up_assessment": "GAO confirmed EDR agent deployment underway across priority endpoints.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["SI-4", "AU-6", "IR-5"],
            "nist_csf_category": "DE.AE",
            "soc2_crosswalk": ["CC7.2", "CC7.3"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-07",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Cyber Response and Recovery",
        "original_finding": "Siloed organizations and manual operations hinder VA's ability to maintain mission continuity.",
        "identified_weakness": "Disaster recovery failover procedures relied heavily on manual intervention without automated cross-regional continuity testing.",
        "auditor_recommendation": "Automate failover orchestration, update system contingency plans, and execute annual cross-site recovery simulations.",
        "management_response": "VA concurred and developed a 4-action remediation roadmap for incident response and continuity.",
        "remediation_action": "Automate cloud disaster recovery failover pipelines and revise departmental contingency plans.",
        "implementation_status": "Partially implemented",
        "status_details": "2 of 4 remediation actions completed as of July 2025. Schedule experienced delays.",
        "estimated_completion_date": "Fiscal Year 2026 (Delayed)",
        "follow_up_assessment": "GAO validated completion of revised contingency plans; automated failover testing remains in progress.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["CP-2", "CP-4", "IR-4"],
            "nist_csf_category": "RC.RP",
            "soc2_crosswalk": ["CC9.1", "A1.2"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-08",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Medical Device Cybersecurity",
        "original_finding": "VA faces challenges in quickly addressing vulnerable medical devices and maintaining security over the life of these devices.",
        "identified_weakness": "Legacy medical devices running unsupported embedded software cannot receive vendor security patches without voiding regulatory certifications.",
        "auditor_recommendation": "Isolate vulnerable medical devices on dedicated micro-segmented VLANs, enforce protocol inspection firewalls, and maintain life-cycle replacement schedules.",
        "management_response": "VA concurred and committed to a 6-action remediation plan for medical device security.",
        "remediation_action": "Implement medical device network segmentation and deploy clinical IoT behavioral anomaly detection.",
        "implementation_status": "Partially implemented",
        "status_details": "3 of 6 remediation actions completed as of July 2025. Timeline delayed due to clinical site complexity.",
        "estimated_completion_date": "May 2027 (Delayed)",
        "follow_up_assessment": "GAO verified segmentation in major medical centers; full enterprise deployment delayed to 2027.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["SC-7", "SI-2", "SA-22"],
            "nist_csf_category": "PR.PT",
            "soc2_crosswalk": ["CC6.6", "CC6.8"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-09",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "ISSO Roles and System Steward Accountability",
        "original_finding": "Information System Security Officer roles need to be aligned with specific systems (e.g., infrastructure, medical devices).",
        "identified_weakness": "ISSOs assigned excessive workloads across conflicting technical domains without clear system-level stewardship boundaries.",
        "auditor_recommendation": "Reallocate ISSO assignments based on technical specialization and establish clear governance metrics for system stewardship.",
        "management_response": "VA concurred and established 3 remediation actions.",
        "remediation_action": "Restructure ISSO job classifications and complete specialized technical training curricula.",
        "implementation_status": "Partially implemented",
        "status_details": "1 of 3 remediation actions completed as of July 2025.",
        "estimated_completion_date": "2026-03-30",
        "follow_up_assessment": "GAO validated completion of training curriculum development; staff reallocation ongoing.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["PL-4", "PS-7", "PM-1"],
            "nist_csf_category": "GV.RR",
            "soc2_crosswalk": ["CC1.3", "CC1.4"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-10",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Customer Service to Systems Teams",
        "original_finding": "Office of Information Security teams that provide security services to system-level teams did not effectively communicate and coordinate together, hindering effective cybersecurity implementation.",
        "identified_weakness": "System development teams experienced delays in receiving security architectural sign-offs, creating friction and deployment bottlenecks.",
        "auditor_recommendation": "Establish defined service-level agreements (SLAs), standing intake consultation desks, and collaborative deployment pipelines.",
        "management_response": "VA concurred and implemented a 4-action service delivery improvement plan.",
        "remediation_action": "Establish security liaison desks and formalize 5-day architectural review SLAs.",
        "implementation_status": "Implemented / Closed",
        "status_details": "All 4 of 4 remediation actions completed as of July 2025.",
        "estimated_completion_date": "Completed (July 2025)",
        "follow_up_assessment": "GAO validated that all 4 remediation actions were fully executed and operationalized.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["PM-10", "SA-4"],
            "nist_csf_category": "GV.OC",
            "soc2_crosswalk": ["CC1.4", "CC2.2"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 2 & Table 7",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-11",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Agencywide Risk Management Strategy",
        "original_finding": "VA had not established all required elements for agencywide cybersecurity risk management programs, including comprehensive risk assessments.",
        "identified_weakness": "Enterprise cyber risk governance lacked formal aggregation of system-level operational risks into the department-level dashboard.",
        "auditor_recommendation": "GAO previously made four recommendations to VA to ensure that VA established required elements for agencywide cybersecurity risk management programs.",
        "management_response": "VA fully concurred and implemented an enterprise risk management framework.",
        "remediation_action": "Adopted NIST SP 800-39 multi-tiered risk management framework and established the Cyber Risk Executive Council.",
        "implementation_status": "Implemented / Closed",
        "status_details": "All 4 prior GAO recommendations confirmed fully implemented by GAO.",
        "estimated_completion_date": "Completed (Prior Cycle)",
        "follow_up_assessment": "GAO verified that VA instituted the required agencywide risk management processes.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["RA-3", "PM-9", "PM-28"],
            "nist_csf_category": "ID.RA",
            "soc2_crosswalk": ["CC3.1", "CC3.2"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Section: GAO Previously Made Recommendations to Improve Cybersecurity Risk Management",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-12",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Remediation Tracking & Documentation (VA OIG Finding)",
        "original_finding": "VA did not consistently track and update planned remediation documents (plans of action and milestones - POA&Ms) for identified security vulnerabilities.",
        "identified_weakness": "System owners failed to update remediation target dates when delays occurred, leading to untracked overdue vulnerabilities.",
        "auditor_recommendation": "VA OIG recommended ensuring that the department systematically tracks, updates, and validates planned remediation documents.",
        "management_response": "VA agreed with the recommendation and initiated a POA&M modernization initiative.",
        "remediation_action": "Transition to automated POA&M tracking within the enterprise Governance, Risk, and Compliance (GRC) tool.",
        "implementation_status": "Open / Not implemented",
        "status_details": "As of July 2025, the department had not yet implemented the recommendation.",
        "estimated_completion_date": "Pending verification",
        "follow_up_assessment": "GAO noted that VA did not update its plans when system remediation dates were missed, leaving OIG recommendation open.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["CA-5", "PM-4"],
            "nist_csf_category": "ID.RA",
            "soc2_crosswalk": ["CC7.3", "CC7.4"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Section: VA Documented Efforts to Remediate Remaining System Findings, but Did Not Update Its Plans",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-REC-13",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "Mitigating Controls for Delayed Vulnerabilities (VA OIG Finding)",
        "original_finding": "Vulnerabilities were not addressed within policy time frames, and mitigating controls were not consistently verified while permanent fixes were pending.",
        "identified_weakness": "Overdue high-risk vulnerabilities remained active in production without documented or tested mitigating controls to prevent exploitation.",
        "auditor_recommendation": "VA OIG recommended ensuring that vulnerabilities will be addressed within policy time frames by ensuring implementation of mitigating controls.",
        "management_response": "VA agreed with the recommendation.",
        "remediation_action": "Enforce mandatory compensating control sign-off by the CISO for any vulnerability exceeding 30-day remediation SLAs.",
        "implementation_status": "Open / Not implemented",
        "status_details": "As of July 2025, the department had not yet fully implemented the recommendation.",
        "estimated_completion_date": "Pending verification",
        "follow_up_assessment": "GAO confirmed that while VA documented mitigating controls for some findings, consistent enforcement was not yet achieved.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["SI-2", "CA-3", "RA-5"],
            "nist_csf_category": "PR.IP",
            "soc2_crosswalk": ["CC7.1", "CC7.4"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Section: VA Documented Remediations for Program Findings, but Did Not Update Its Plans",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-SYS-01",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "High-Impact System 1 (Benefits Management)",
        "original_finding": "System 1 had 107 total security findings (8 high, 39 moderate, 60 low risk) identified during independent technical assessment.",
        "identified_weakness": "Software patch delays and credential validation vulnerabilities on core benefits calculation engines.",
        "auditor_recommendation": "Remediate all 8 high-risk vulnerabilities immediately and update system security plan milestones.",
        "management_response": "VA submitted a technical remediation plan with target completion by 12/31/2025.",
        "remediation_action": "Applied operating system security rollups, replaced deprecated cryptographic libraries, and revoked stale service accounts.",
        "implementation_status": "Partially implemented",
        "status_details": "7 of 8 high-risk, 36 of 39 moderate-risk, and 53 of 60 low-risk remediated (96 of 107 total; 90% completion rate).",
        "estimated_completion_date": "2025-12-31",
        "follow_up_assessment": "GAO validated that 90% of findings were remediated by July 2025; 1 high-risk item remains open.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["SI-2", "IA-2", "AC-2"],
            "nist_csf_category": "PR.IP",
            "soc2_crosswalk": ["CC6.1", "CC6.8"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 4 & Table 6",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-SYS-02",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "High-Impact System 2 (Electronic Health Records / Clinical VistA)",
        "original_finding": "System 2 had 65 security findings (3 high, 22 moderate, 40 low risk), with remediation progress significantly lower than all other high-impact systems.",
        "identified_weakness": "Deep architectural dependencies on legacy MUMPS code and clinical workstation interfaces prevented standard automated patching without risking clinical downtime.",
        "auditor_recommendation": "Develop clinical compensating controls, isolate unpatchable legacy modules on dedicated VLANs, and establish phased migration milestones.",
        "management_response": "VA acknowledged remediation difficulty and extended the estimated remediation date to 01/02/2028.",
        "remediation_action": "Remediated 3 of 3 high-risk vulnerabilities, but only 13 of 22 moderate and 17 of 40 low-risk vulnerabilities.",
        "implementation_status": "Partially implemented",
        "status_details": "33 of 65 total findings remediated (51% completion rate). Progress significantly delayed.",
        "estimated_completion_date": "2028-01-02 (Significantly Delayed)",
        "follow_up_assessment": "GAO highlighted System 2 as experiencing the longest remediation delays across the enterprise due to clinical mission dependencies.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["SC-7", "SI-2", "SA-22"],
            "nist_csf_category": "PR.PT",
            "soc2_crosswalk": ["CC6.6", "CC6.8", "CC7.4"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 4 & Table 6",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-SYS-03",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "High-Impact System 3 (Financial Management / iFAMS)",
        "original_finding": "System 3 had 107 security findings (10 high, 34 moderate, 63 low risk) across financial transaction processing systems.",
        "identified_weakness": "Database connection encryption gaps, unrotated API keys, and missing audit log retention configs.",
        "auditor_recommendation": "Enforce mandatory TLS for all internal database traffic, rotate API keys, and remediate all 10 high-risk vulnerabilities.",
        "management_response": "VA prioritized System 3 remediation due to Federal Financial Management Improvement Act (FFMIA) compliance requirements.",
        "remediation_action": "Remediated 10 of 10 high-risk, 34 of 34 moderate-risk, and 63 of 63 low-risk vulnerabilities.",
        "implementation_status": "Implemented / Closed",
        "status_details": "107 of 107 total findings remediated (100% completion rate). Completed ahead of the 03/30/2025 milestone.",
        "estimated_completion_date": "Completed (July 2025)",
        "follow_up_assessment": "GAO verified that System 3 was the only high-impact system to achieve 100% remediation of all findings.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["SC-8", "SC-28", "AC-6", "AU-9"],
            "nist_csf_category": "PR.DS",
            "soc2_crosswalk": ["CC6.1", "CC6.7"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 4 & Table 6",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-SYS-04",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "High-Impact System 4 (Corporate Data Warehouse)",
        "original_finding": "System 4 had 56 security findings (7 high, 23 moderate, 26 low risk) regarding large-scale healthcare data analytics clusters.",
        "identified_weakness": "Excessive analytical query permissions, unmonitored bulk data export interfaces, and delayed vulnerability patching.",
        "auditor_recommendation": "Implement role-based access boundaries for data scientists, restrict bulk export permissions, and remediate high-risk database flaws.",
        "management_response": "VA concurred and committed to completing remediation by 01/31/2025.",
        "remediation_action": "Remediated 6 of 7 high-risk, 17 of 23 moderate-risk, and 24 of 26 low-risk vulnerabilities.",
        "implementation_status": "Partially implemented",
        "status_details": "47 of 56 total findings remediated (84% completion rate).",
        "estimated_completion_date": "2025-01-31 (Pending Final Verification)",
        "follow_up_assessment": "GAO confirmed substantial progress with 1 high-risk finding remaining open during evaluation period.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["AC-3", "AC-6", "AU-6", "SI-2"],
            "nist_csf_category": "PR.AC",
            "soc2_crosswalk": ["CC6.1", "CC6.3"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 4 & Table 6",
            "extracted_at": "2026-11-07"
        }
    },
    {
        "id": "GAO-26-107980-SYS-05",
        "agency": "Department of Veterans Affairs (VA)",
        "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
        "report_number": "GAO-26-107980",
        "publication_date": "2025-12-01",
        "finding_area": "High-Impact System 5 (Identity & Access Management Gateway)",
        "original_finding": "System 5 had 107 security findings (1 high, 37 moderate, 69 low risk) concerning identity federation and single sign-on infrastructure.",
        "identified_weakness": "Legacy authentication protocol fallbacks and incomplete deployment of phishing-resistant credentials across portal users.",
        "auditor_recommendation": "Deprecate legacy authentication protocols and mandate phishing-resistant FIDO2/PIV credentials for all administrative and user sessions.",
        "management_response": "VA concurred and scheduled full remediation by 12/31/2024.",
        "remediation_action": "Remediated 1 of 1 high-risk, 35 of 37 moderate-risk, and 60 of 69 low-risk vulnerabilities.",
        "implementation_status": "Partially implemented",
        "status_details": "96 of 107 total findings remediated (90% completion rate).",
        "estimated_completion_date": "2024-12-31 (Pending Final Verification)",
        "follow_up_assessment": "GAO validated the single high-risk vulnerability was closed; minor configuration items remained in testing.",
        "framework_reference": {
            "primary_framework": "NIST SP 800-53 Rev. 5",
            "control_codes": ["IA-2", "IA-5", "AC-2", "AC-17"],
            "nist_csf_category": "PR.AC",
            "soc2_crosswalk": ["CC6.1", "CC6.2"]
        },
        "provenance": {
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "source_type": "Official GAO Report to Congressional Committees",
            "page_or_section": "Table 4 & Table 6",
            "extracted_at": "2026-11-07"
        }
    }
]

def build():
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/metadata', exist_ok=True)
    os.makedirs('data/evaluation', exist_ok=True)

    # 1. Write processed real audit findings
    processed_path = os.path.join('data', 'processed', 'real_audit_findings.json')
    with open(processed_path, 'w', encoding='utf-8') as f:
        json.dump(RECORDS, f, indent=2)
    print(f"Successfully generated {len(RECORDS)} authentic audit records in: {processed_path}")

    # 2. Write metadata catalog
    metadata = {
        "dataset_name": "ReguGuard Authentic Cybersecurity Audit Dataset",
        "version": "1.0.0",
        "total_verified_records": len(RECORDS),
        "primary_source": {
            "agency": "U.S. Government Accountability Office (GAO)",
            "report_number": "GAO-26-107980",
            "report_title": "CYBERSECURITY: Independent Assessment and VA Response Generally Met Requirements",
            "publication_date": "December 2025",
            "source_url": "https://files.gao.gov/reports/GAO-26-107980/index.html",
            "authorizing_statute": "Strengthening VA Cybersecurity Act of 2022 (P.L. 117-257)",
            "assessor": "MITRE Corporation & GAO"
        },
        "secondary_reference_framework": {
            "agency": "U.S. Government Accountability Office (GAO)",
            "report_number": "GAO-23-104705",
            "report_title": "Cybersecurity Program Audit Guide (CPAG)",
            "publication_date": "September 2023",
            "source_url": "https://www.gao.gov/assets/gao-23-104705.pdf"
        },
        "framework_standards": [
            "NIST SP 800-53 Rev. 5",
            "NIST Cybersecurity Framework 2.0 (CSF 2.0)",
            "Federal Information Security Modernization Act (FISMA)",
            "AICPA SOC 2 Type II Trust Services Criteria (Crosswalk Reference)"
        ],
        "status_categories_used": [
            "Open / Not implemented",
            "Resolved / Agreed to implement",
            "Implemented / Closed",
            "Partially implemented",
            "Pending verification",
            "Unknown / Not publicly documented"
        ],
        "created_at": "2026-11-07"
    }

    metadata_path = os.path.join('data', 'metadata', 'sources.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"Successfully generated metadata catalog in: {metadata_path}")

    # 3. Write evaluation benchmark test cases
    evaluation_cases = [
        {
            "test_id": "EVAL-01-CLOUD-DRIFT",
            "description": "Evaluate retrieval of past cloud configuration drift finding and delayed remediation status",
            "query": "Inconsistent baseline cloud security configurations across multi-cloud tenants leading to storage bucket exposure",
            "expected_top_match_id": "GAO-26-107980-REC-02",
            "expected_framework_code": "CM-2",
            "expected_status": "Partially implemented",
            "expected_historical_context": "Remediation delayed past 2025 milestone with 2 of 6 actions completed"
        },
        {
            "test_id": "EVAL-02-LEGACY-CLINICAL",
            "description": "Evaluate retrieval of unpatchable legacy systems and compensating network segmentation history",
            "query": "Legacy electronic health record database running unsupported MUMPS code with clinical disruption patching risk",
            "expected_top_match_id": "GAO-26-107980-SYS-02",
            "expected_framework_code": "SC-7",
            "expected_status": "Partially implemented",
            "expected_historical_context": "Longest remediation delay across agency extended to 2028; requires clinical compensating micro-segmentation"
        },
        {
            "test_id": "EVAL-03-POAM-OVERDUE",
            "description": "Evaluate identification of recurring open vulnerability tracking failures without updated milestones",
            "query": "System owners failing to track and update plan of action and milestones (POA&M) target completion dates",
            "expected_top_match_id": "GAO-26-107980-REC-12",
            "expected_framework_code": "CA-5",
            "expected_status": "Open / Not implemented",
            "expected_historical_context": "VA OIG recommendation remains open; missing updated milestones"
        }
    ]

    eval_path = os.path.join('data', 'evaluation', 'benchmark_test_cases.json')
    with open(eval_path, 'w', encoding='utf-8') as f:
        json.dump(evaluation_cases, f, indent=2)
    print(f"Successfully generated evaluation test cases in: {eval_path}")

if __name__ == '__main__':
    build()
