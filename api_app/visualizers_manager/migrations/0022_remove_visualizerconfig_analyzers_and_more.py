# Generated by Django 4.1.9 on 2023-06-22 07:07

from django.db import migrations, models


def _migrate_custom_visualizers(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    PlaybookConfig = apps.get_model("playbooks_manager", "PlaybookConfig")
    for i, vc in enumerate(
        VisualizerConfig.objects.exclude(
            name__in=["Domain_Reputation", "IP_Reputation", "DNS", "Yara"]
        )
    ):
        try:
            pc = PlaybookConfig.objects.get(
                analyzers__in=vc.analyzers.all(),
                connectors__in=vc.connectors.all(),
            )
        except PlaybookConfig.DoesNotExist:
            pc = PlaybookConfig.objects.create(
                name=f"CustomPlaybook{i}",
                type=["ip", "url", "domain", "hash", "generic", "file"],
            )
            pc.analyzers.set(vc.analyzers.all())
            pc.connectors.set(vc.connectors.all())
        vc.playbook = pc
        vc.save()


def _reverse_migrate_custom_visualizers(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    for vc in VisualizerConfig.objects.exclude(
        name__in=["Domain_Reputation", "IP_Reputation", "DNS", "Yara"]
    ):
        pc = vc.playbook
        vc.analyzers = pc.analyzers
        vc.connectors = pc.connectors
        vc.save()


def _migrate_domain_reputation(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    PlaybookConfig = apps.get_model("playbooks_manager", "PlaybookConfig")
    vc = VisualizerConfig.objects.get(name="Domain_Reputation")
    vc.playbook = PlaybookConfig.objects.get(name="Popular_URL_Reputation_Services")
    vc.full_clean()
    vc.save()


def _reverse_migrate_domain_reputation(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    AnalyzerConfig = apps.get_model("analyzers_manager", "AnalyzerConfig")
    vc = VisualizerConfig.objects.get(name="Domain_Reputation")
    vc.analyzers.set(
        [
            AnalyzerConfig.objects.get(name="ThreatFox"),
            AnalyzerConfig.objects.get(name="DNS0_EU_Malicious_Detector"),
            AnalyzerConfig.objects.get(name="Quad9_Malicious_Detector"),
            AnalyzerConfig.objects.get(name="OTXQuery"),
            AnalyzerConfig.objects.get(name="Phishtank"),
            AnalyzerConfig.objects.get(name="CloudFlare_Malicious_Detector"),
            AnalyzerConfig.objects.get(name="URLhaus"),
            AnalyzerConfig.objects.get(name="VirusTotal_v3_Get_Observable"),
            AnalyzerConfig.objects.get(name="PhishingArmy"),
            AnalyzerConfig.objects.get(name="InQuest_REPdb"),
            AnalyzerConfig.objects.get(name="GoogleSafebrowsing"),
        ]
    )
    vc.save()


def _migrate_ip_reputation(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    PlaybookConfig = apps.get_model("playbooks_manager", "PlaybookConfig")
    vc = VisualizerConfig.objects.get(name="IP_Reputation")
    vc.playbook = PlaybookConfig.objects.get(name="Popular_IP_Reputation_Services")
    vc.full_clean()
    vc.save()


def _reverse_migrate_ip_reputation(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    AnalyzerConfig = apps.get_model("analyzers_manager", "AnalyzerConfig")
    vc = VisualizerConfig.objects.get(name="IP_Reputation")
    vc.analyzers.set(
        [
            AnalyzerConfig.objects.get(name="TalosReputation"),
            AnalyzerConfig.objects.get(name="Crowdsec"),
            AnalyzerConfig.objects.get(name="OTXQuery"),
            AnalyzerConfig.objects.get(name="TorProject"),
            AnalyzerConfig.objects.get(name="AbuseIPDB"),
            AnalyzerConfig.objects.get(name="GreedyBear"),
            AnalyzerConfig.objects.get(name="VirusTotal_v3_Get_Observable"),
            AnalyzerConfig.objects.get(name="FireHol_IPList"),
            AnalyzerConfig.objects.get(name="URLhaus"),
            AnalyzerConfig.objects.get(name="ThreatFox"),
            AnalyzerConfig.objects.get(name="InQuest_REPdb"),
            AnalyzerConfig.objects.get(name="GreyNoiseCommunity"),
        ]
    )
    vc.save()


def _migrate_dns(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    PlaybookConfig = apps.get_model("playbooks_manager", "PlaybookConfig")
    visualizer = VisualizerConfig.objects.get(name="DNS")
    visualizer.playbook = PlaybookConfig.objects.get(name="Dns")
    visualizer.full_clean()
    visualizer.save()


def _reverse_migrate_dns(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    AnalyzerConfig = apps.get_model("analyzers_manager", "AnalyzerConfig")
    visualizer = VisualizerConfig.objects.get(name="DNS")
    visualizer.analyzers.set(
        [
            AnalyzerConfig.objects.get(name="Classic_DNS"),
            AnalyzerConfig.objects.get(name="CloudFlare_DNS"),
            AnalyzerConfig.objects.get(name="DNS0_EU"),
            AnalyzerConfig.objects.get(name="Google_DNS"),
            AnalyzerConfig.objects.get(name="Quad9_DNS"),
            AnalyzerConfig.objects.get(name="CloudFlare_Malicious_Detector"),
            AnalyzerConfig.objects.get(name="DNS0_EU_Malicious_Detector"),
            AnalyzerConfig.objects.get(name="Quad9_Malicious_Detector"),
        ]
    )
    visualizer.full_clean()
    visualizer.save()


def _migrate_yara(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    PlaybookConfig = apps.get_model("playbooks_manager", "PlaybookConfig")
    visualizer = VisualizerConfig.objects.get(name="Yara")
    visualizer.playbook = PlaybookConfig.objects.get(name="Sample_Static_Analysis")
    visualizer.full_clean()
    visualizer.save()


def _reverse_migrate_yara(apps):
    VisualizerConfig = apps.get_model("visualizers_manager", "VisualizerConfig")
    AnalyzerConfig = apps.get_model("analyzers_manager", "AnalyzerConfig")
    visualizer = VisualizerConfig.objects.get(name="Yara")
    visualizer.analyzers.set(
        [
            AnalyzerConfig.objects.get(name="Yara"),
        ]
    )
    visualizer.full_clean()
    visualizer.save()


def migrate(apps, schema_editor):
    _migrate_yara(apps)
    _migrate_dns(apps)
    _migrate_ip_reputation(apps)
    _migrate_domain_reputation(apps)
    _migrate_custom_visualizers(apps)


def reverse_migrate(apps, schema_editor):
    _reverse_migrate_yara(apps)
    _reverse_migrate_dns(apps)
    _reverse_migrate_ip_reputation(apps)
    _reverse_migrate_domain_reputation(apps)
    _reverse_migrate_custom_visualizers(apps)


class Migration(migrations.Migration):

    dependencies = [
        ("playbooks_manager", "0015_dns_playbook"),
        ("visualizers_manager", "0021_alter_visualizerconfig_options"),
        ("analyzers_manager", "0030_alter_analyzerconfig_options"),
        ("connectors_manager", "0017_alter_connectorconfig_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="visualizerconfig",
            name="playbook",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.CASCADE,
                related_name="visualizers",
                to="playbooks_manager.playbookconfig",
            ),
        ),
        migrations.RunPython(migrate, reverse_migrate),
        migrations.AlterField(
            model_name="visualizerconfig",
            name="playbook",
            field=models.ForeignKey(
                blank=False,
                null=False,
                on_delete=models.CASCADE,
                related_name="visualizers",
                to="playbooks_manager.playbookconfig",
            ),
        ),
        migrations.RemoveField(
            model_name="visualizerconfig",
            name="analyzers",
        ),
        migrations.RemoveField(
            model_name="visualizerconfig",
            name="connectors",
        ),
    ]
