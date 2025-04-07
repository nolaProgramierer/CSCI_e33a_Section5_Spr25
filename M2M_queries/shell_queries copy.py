# 1) Creating employees
# --------------------
alice = Employee.objects.create(fname="Alice", lname="Johnson")
bob = Employee.objects.create(fname="Bob", lname="Smith")
carol = Employee.objects.create(fname="Carol", lname="Davis")
dave = Employee.objects.create(fname="Dave", lname="Miller")


# 2) Assign Supervisors
# ---------------------
# Assign Bob and Carol to be supervised by Alice
alice.subordinates.add(bob, carol)

# Assign Dave to supervise Alice
dave.subordinates.add(alice)


# 3) Get All Supervisors of a Specific Employee
# ---------------------------------------------
# Find all supervisors of Bob
bob_supervisors = bob.supervisors.all()  # Should return Alice


# 4) Get All Subordinates of a Specific Employee
# ----------------------------------------------
# Find all subordinates of Alice
alice_subordinates = alice.subordinates.all()  # Should return Bob and Carol


# 5) Check if an Employee Has Supervisors
# ---------------------------------------
# Check if Bob has any supervisors
bob_has_supervisors = bob.supervisors.exists()  # Should return True


# 6) Get Subordinates for a Specific Employee
# -------------------------------------------
# Get all subordinates of Alice
alice_subordinates = alice.subordinates.all()


# 7) Count the Number of Subordinates for a Specific Supervisor
# -------------------------------------------------------------
# Count how many subordinates Alice has
alice_subordinate_count = alice.subordinates.count()  # Should return 2


# 8) Find Employees Without Any Supervisors
# -----------------------------------------
# Find all employees with no supervisors
employees_with_no_supervisors = Employee.objects.filter(supervisors__isnull=True)  


# 9) Find Employees Without Any Subordinates
# ------------------------------------------
# Find all employees who do not supervise anyone
employees_with_no_subordinates = Employee.objects.filter(subordinates__isnull=True)


# 10) Find all employees with no supervisors and no subordinates
orphaned_employees = Employee.objects.filter(subordinates__isnull=True, supervisors__isnull=True)


# 11) Find the top level employee (no supervisor)
is_boss = dave.is_top_level_employee()


# 12) Find employees with most subordinates
bosses = Employee.objects.annotate(num_subordinates=Count('subordinates')).order_by('-num_subordinates')


# 13) Remove a Supervisor from an Employee
# ----------------------------------------
# Remove Alice as Bob's supervisor
bob.supervisors.remove(alice)


# 14) Clear All Subordinates of a Supervisor
# ------------------------------------------
# Remove all subordinates from Alice
alice.subordinates.clear()


















