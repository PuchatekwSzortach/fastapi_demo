"""
Module with invoke tasks
"""

import invoke


import scripts.invoke.docker
import scripts.invoke.run
import scripts.invoke.tests

# Default invoke collection
ns = invoke.Collection()

# Add collections defined in other files
ns.add_collection(scripts.invoke.docker)
ns.add_collection(scripts.invoke.run)
ns.add_collection(scripts.invoke.tests)
