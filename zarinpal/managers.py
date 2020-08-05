from django.db import models 

class PaymentTransactionQueryset(models.QuerySet):
    def pend(self):
        return self.filter(status='P')
    
    def fail(self):
        return self.filter(status='F')
    
    def notcomplete(self):
        pend = self.pend()
        fail = self.fail()
        onion = self.none()
        onion = onion.union(pend, fail) # MAGIC ONION
        return onion

class PaymentTransactionManager(models.Manager):
    def get_queryset(self):
        return PaymentTransactionQueryset(self.model, using=self._db)

    def pend(self):
        return self.get_queryset().pend()

    def fail(self):
        return self.get_queryset().fail()

    def notcomplete(self):
        return self.get_queryset().notcomplete()