# Copyright 2013 Rooter Analysis S.L.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from adminsortable.models import Sortable
from tinymce.models import HTMLField

from moocng.courses.models import KnowledgeQuantum
from moocng.peerreview import cache
from moocng.peerreview.managers import PeerReviewAssignmentManager


class PeerReviewAssignment(models.Model):
    description = HTMLField(verbose_name=_(u'Description'),
                            blank=True, null=False)
    minimum_reviewers = models.PositiveSmallIntegerField(verbose_name=_(u'Minimum reviewers'))
    kq = models.ForeignKey(KnowledgeQuantum,
                           verbose_name=_(u'Nugget'),
                           blank=False, null=False)
    objects = PeerReviewAssignmentManager()

    class Meta:
        verbose_name = _(u'peer review assignment')
        verbose_name_plural = _(u'peer review assignments')

    def __unicode__(self):
        return self.kq.__unicode__()

def invalidate_cache(sender, instance, **kwargs):
    course = instance.kq.unit.course
    cache.invalidate_course_has_peer_review_assignment_in_cache(course)


signals.post_save.connect(invalidate_cache, sender=PeerReviewAssignment)
signals.post_delete.connect(invalidate_cache, sender=PeerReviewAssignment)


class EvaluationCriterion(Sortable):
    assignment = models.ForeignKey(PeerReviewAssignment,
                                   verbose_name=_(u'Peer review assignment'),
                                   related_name='criteria')
    title = models.CharField(verbose_name=_(u'Title'), max_length=100,
                            blank=False, null=False)
    description = models.TextField(verbose_name=_(u'Description'),
                                   blank=True, null=False)

    class Meta(Sortable.Meta):
        verbose_name = _(u'evaluation criterion')
        verbose_name_plural = _(u'evaluation criteria')

    def __unicode__(self):
        return ugettext(u'{0} - EvaluationCriteria {1}').format(self.assignment, self.id)
