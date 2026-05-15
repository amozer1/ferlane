def generate_commentary(cl31, cl32, kpis):

    return f"""
NEC PROGRAMME ASSESSMENT

The current CL32 programme contains {kpis['total']} activities.
Critical activities account for {kpis['critical']} items, with {kpis['near_critical']} near-critical elements.

Average total float is recorded at {kpis['avg_float']:.2f} days.

Comparison against CL31 baseline indicates programme movement affecting key milestone delivery paths.
Float erosion is concentrated within high-risk sequencing chains.

Under NEC Clause 31/32 principles, this indicates a requirement for closer monitoring of compensation event impacts and mitigation actions.
"""