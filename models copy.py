from django.db import models
from django.core.exceptions import ValidationError

# -----------------------------------------------------------------
# Recursive m2m
# ------------------------------------------------------------------

class Employee(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=25)
    supervisors = models.ManyToManyField("Employee", related_name="subordinates")

    class Meta:
        """ Default ordering of Employee objects """
        ordering = ["lname"]

    def __str__(self):
        """ Return a string representation of the object """
        return f"{self.lname}, {self.fname}"
    
    def is_top_level_employee(self):
        """ Return employee with no supervisors """
        return not self.supervisors.exists()
    
        
    


    
    




