from django.db import models
from Test.models import *
from task1b.models import *
# Create your models here.
from datetime import datetime



class eval_measi_oracle_1bb(models.Model):
        testset=models.ForeignKey(Detail1b)
        system=models.ForeignKey(system)
        acc=models.FloatField(null=True, blank=True, verbose_name="yes/no: accuracy")
        s_acc=models.FloatField(null=True, blank=True, verbose_name="factoid: strict accuracy")
        l_acc=models.FloatField(null=True, blank=True, verbose_name="factoid: lenient accuracy")
        mrr=models.FloatField(null=True, blank=True, verbose_name="factoid: MRR")
        prec=models.FloatField(null=True, blank=True, verbose_name="list: mean precision")
        rec=models.FloatField(null=True, blank=True, verbose_name="list: mean recall")
        fmeas=models.FloatField(null=True, blank=True, verbose_name="list: f measure")
        r2p=models.FloatField(null=True, blank=True, verbose_name="ROUGE2: precision")
        r2r=models.FloatField(null=True, blank=True, verbose_name="ROUGE2: recall")
        r2f=models.FloatField(null=True, blank=True, verbose_name="ROUGE2: f measure")
        r4p=models.FloatField(null=True, blank=True, verbose_name="ROUGE-SU4: precision")
        r4r=models.FloatField(null=True, blank=True, verbose_name="ROUGE-SU4: recall")
        r4f=models.FloatField(null=True, blank=True, verbose_name="ROUGE-SU4: f measure")
        read=models.FloatField(null=True, blank=True, verbose_name="Readability")
        recall=models.FloatField(null=True, blank=True, verbose_name="Recall")
        rep=models.FloatField(null=True, blank=True, verbose_name="Repetition")
        preci=models.FloatField(null=True, blank=True, verbose_name="Precision")
	timestamp=models.DateTimeField(default=datetime.now())
        is_visible=models.BooleanField(default=True)
        class Meta:
                verbose_name="Evaluation measures for 1B, phase B"
                verbose_name_plural=verbose_name


class eval_meas_oracle(models.Model):
        user=models.ForeignKey(system, verbose_name="the participating system")
        test_id=models.ForeignKey(Detail, verbose_name="the related test set")
        accuracy=models.FloatField()
        ebp=models.FloatField(verbose_name="example based precision")
        example_based_recall=models.FloatField()
        example_based_f=models.FloatField(verbose_name="example based f-measure")
        macro_precision=models.FloatField()
        macro_recall=models.FloatField()
        macro_f_measure=models.FloatField(verbose_name="macro f-measure")
        micro_precision=models.FloatField()
        micro_recall=models.FloatField()
        micro_f=models.FloatField(verbose_name="micro f-measure")
        hierarchical_precision=models.FloatField()
        hierarchical_recall=models.FloatField()
        hierarchical_f=models.FloatField(verbose_name="hierarchical F-measure")
        lca_p=models.FloatField(verbose_name="lca Precision")
        lca_r=models.FloatField(verbose_name="lca Recall")
        lca_f=models.FloatField(verbose_name="lca F-measure")
	timestamp=models.DateTimeField(default=datetime.now())
        is_visible=models.BooleanField(default=True)
        class Meta:
                verbose_name="Evaluation Measure"
                verbose_name_plural="Evaluation Measures for the oracle"


class eval_meas_oracle_1b(models.Model):
        test_id=models.ForeignKey(Detail1b)
        user=models.ForeignKey(system)
        mp_con=models.FloatField(null=True, blank=True, verbose_name="concepts: mean precision")
        mr_con=models.FloatField(null=True, blank=True, verbose_name="concepts: recall")
        f_con=models.FloatField(null=True, blank=True, verbose_name="concepts: f-measure")
        MAP_con=models.FloatField(null=True, blank=True, verbose_name="concepts: MAP")
        GMAP_con=models.FloatField(null=True, blank=True, verbose_name="concepts: GMAP")
        mp_art=models.FloatField(null=True, blank=True, verbose_name="articles:mean precision")
        mr_art=models.FloatField(null=True, blank=True, verbose_name="articles:recall")
        f_art=models.FloatField(null=True, blank=True, verbose_name="articles:f-measure")
        MAP_art=models.FloatField(null=True, blank=True, verbose_name="articles: MAP")
        GMAP_art=models.FloatField(null=True, blank=True, verbose_name="articles:GMAP")
        mp_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: mean precision")
        mr_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: recall")
        f_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: f-measure")
        MAP_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: MAP")
        GMAP_snip=models.FloatField(null=True, blank=True, verbose_name="snippets: GMAP")
        mp_trip=models.FloatField(null=True, blank=True, verbose_name="triples: mean precision")
        mr_trip=models.FloatField(null=True, blank=True, verbose_name="triples: recall")
        f_trip=models.FloatField(null=True, blank=True, verbose_name="triples: f-measure")
        MAP_trip=models.FloatField(null=True, blank=True, verbose_name="triples: MAP")
        GMAP_trip=models.FloatField(null=True, blank=True, verbose_name="triples: GMAP")
	timestamp=models.DateTimeField(default=datetime.now())
        is_visible=models.BooleanField(default=True)
        class Meta:
                verbose_name="Evaluation Measure for Task 1b phase A"
                verbose_name_plural="Evaluation Measures for Task 1b phase A"




class log_oracle(models.Model):
        user=models.ForeignKey(User)
        system=models.ForeignKey(system)
        test_id=models.ForeignKey(Detail)
        timestamp=models.DateTimeField()
        comment=models.CharField(max_length=1900, null=True, blank=True)
        class Meta:
                verbose_name="Upload Information/Log"
                verbose_name_plural=verbose_name
