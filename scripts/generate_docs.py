#!/usr/bin/env python3
"""
Complete PGA Tour GraphQL API Documentation Generator
Generates 100% coverage documentation of all types, queries, mutations, etc.
"""

import json
import os

def load_schema():
    # Look for schema in multiple locations
    paths = [
        "schema/schema.json",
        "../schema/schema.json",
        "pga_schema_raw.json"
    ]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    raise FileNotFoundError("Schema file not found. Run introspect.py first.")

def format_type_ref(type_ref, depth=0):
    """Format a type reference into a readable string."""
    if type_ref is None or depth > 10:
        return "Unknown"

    kind = type_ref.get("kind")
    name = type_ref.get("name")
    of_type = type_ref.get("ofType")

    if kind == "NON_NULL":
        return f"{format_type_ref(of_type, depth+1)}!"
    elif kind == "LIST":
        return f"[{format_type_ref(of_type, depth+1)}]"
    elif name:
        return name
    else:
        return "Unknown"

def get_type_link(type_ref, depth=0):
    """Get the base type name for linking."""
    if type_ref is None or depth > 10:
        return None

    kind = type_ref.get("kind")
    name = type_ref.get("name")
    of_type = type_ref.get("ofType")

    if kind in ["NON_NULL", "LIST"]:
        return get_type_link(of_type, depth+1)
    elif name and not name.startswith("__"):
        return name
    return None

def generate_queries_doc(schema):
    """Generate complete queries documentation."""
    types = schema.get("types", [])
    query_type_name = schema.get("queryType", {}).get("name", "Query")
    query_type = next((t for t in types if t["name"] == query_type_name), None)

    if not query_type:
        return ""

    doc = []
    doc.append("# PGA Tour GraphQL API - Complete Queries Reference\n\n")
    doc.append(f"**Total Queries: {len(query_type.get('fields', []))}**\n\n")
    doc.append("---\n\n")
    doc.append("## Table of Contents\n\n")

    # Generate TOC
    for field in sorted(query_type.get("fields", []), key=lambda x: x["name"]):
        doc.append(f"- [{field['name']}](#{field['name'].lower()})\n")

    doc.append("\n---\n\n")

    # Generate detailed docs for each query
    for field in sorted(query_type.get("fields", []), key=lambda x: x["name"]):
        doc.append(f"## {field['name']}\n\n")

        if field.get("description"):
            doc.append(f"{field['description']}\n\n")

        if field.get("isDeprecated"):
            reason = field.get("deprecationReason", "No reason provided")
            doc.append(f"**⚠️ DEPRECATED:** {reason}\n\n")

        # Arguments
        if field.get("args"):
            doc.append("### Arguments\n\n")
            doc.append("| Name | Type | Required | Description |\n")
            doc.append("|------|------|----------|-------------|\n")
            for arg in field["args"]:
                arg_type = format_type_ref(arg["type"])
                required = "Yes" if arg_type.endswith("!") else "No"
                desc = (arg.get("description") or "").replace("\n", " ").replace("|", "\\|")
                default = f" (default: `{arg['defaultValue']}`)" if arg.get("defaultValue") else ""
                doc.append(f"| `{arg['name']}` | `{arg_type}` | {required} | {desc}{default} |\n")
            doc.append("\n")
        else:
            doc.append("### Arguments\n\nNone\n\n")

        # Return type
        return_type = format_type_ref(field["type"])
        base_type = get_type_link(field["type"])
        doc.append(f"### Returns\n\n`{return_type}`")
        if base_type:
            doc.append(f" → [See {base_type}](./types/{base_type}.md)")
        doc.append("\n\n")

        # Example query
        doc.append("### Example Query\n\n```graphql\nquery {\n")
        if field.get("args"):
            args_str = ", ".join([f"${a['name']}: {format_type_ref(a['type'])}" for a in field["args"]])
            call_args = ", ".join([f"{a['name']}: ${a['name']}" for a in field["args"]])
            doc.append(f"  {field['name']}({call_args}) {{\n")
        else:
            doc.append(f"  {field['name']} {{\n")
        doc.append("    # ... fields\n  }\n}\n```\n\n")

        doc.append("---\n\n")

    return "".join(doc)

def generate_mutations_doc(schema):
    """Generate complete mutations documentation."""
    types = schema.get("types", [])
    mutation_type_name = schema.get("mutationType", {}).get("name")

    if not mutation_type_name:
        return "# PGA Tour GraphQL API - Mutations Reference\n\nNo mutations available.\n"

    mutation_type = next((t for t in types if t["name"] == mutation_type_name), None)

    if not mutation_type:
        return ""

    doc = []
    doc.append("# PGA Tour GraphQL API - Complete Mutations Reference\n\n")
    doc.append(f"**Total Mutations: {len(mutation_type.get('fields', []))}**\n\n")
    doc.append("---\n\n")
    doc.append("## Table of Contents\n\n")

    for field in sorted(mutation_type.get("fields", []), key=lambda x: x["name"]):
        doc.append(f"- [{field['name']}](#{field['name'].lower()})\n")

    doc.append("\n---\n\n")

    for field in sorted(mutation_type.get("fields", []), key=lambda x: x["name"]):
        doc.append(f"## {field['name']}\n\n")

        if field.get("description"):
            doc.append(f"{field['description']}\n\n")

        if field.get("args"):
            doc.append("### Arguments\n\n")
            doc.append("| Name | Type | Required | Description |\n")
            doc.append("|------|------|----------|-------------|\n")
            for arg in field["args"]:
                arg_type = format_type_ref(arg["type"])
                required = "Yes" if arg_type.endswith("!") else "No"
                desc = (arg.get("description") or "").replace("\n", " ").replace("|", "\\|")
                doc.append(f"| `{arg['name']}` | `{arg_type}` | {required} | {desc} |\n")
            doc.append("\n")

        return_type = format_type_ref(field["type"])
        doc.append(f"### Returns\n\n`{return_type}`\n\n")
        doc.append("---\n\n")

    return "".join(doc)

def generate_type_doc(type_obj):
    """Generate documentation for a single object type."""
    doc = []
    doc.append(f"# {type_obj['name']}\n\n")

    if type_obj.get("description"):
        doc.append(f"{type_obj['description']}\n\n")

    doc.append(f"**Kind:** {type_obj['kind']}\n\n")

    # Interfaces
    if type_obj.get("interfaces"):
        interfaces = [format_type_ref(i) for i in type_obj["interfaces"]]
        if interfaces:
            doc.append(f"**Implements:** {', '.join(interfaces)}\n\n")

    # Fields
    if type_obj.get("fields"):
        doc.append("## Fields\n\n")
        doc.append("| Field | Type | Description |\n")
        doc.append("|-------|------|-------------|\n")

        for field in type_obj["fields"]:
            field_type = format_type_ref(field["type"])
            desc = (field.get("description") or "").replace("\n", " ").replace("|", "\\|")
            deprecated = " ⚠️ DEPRECATED" if field.get("isDeprecated") else ""

            # Handle field arguments
            if field.get("args"):
                args_str = ", ".join([f"{a['name']}: {format_type_ref(a['type'])}" for a in field["args"]])
                doc.append(f"| `{field['name']}({args_str})` | `{field_type}` | {desc}{deprecated} |\n")
            else:
                doc.append(f"| `{field['name']}` | `{field_type}` | {desc}{deprecated} |\n")

        doc.append("\n")

        # Detailed field info with args
        fields_with_args = [f for f in type_obj["fields"] if f.get("args")]
        if fields_with_args:
            doc.append("## Field Arguments\n\n")
            for field in fields_with_args:
                doc.append(f"### {field['name']}\n\n")
                doc.append("| Argument | Type | Description |\n")
                doc.append("|----------|------|-------------|\n")
                for arg in field["args"]:
                    arg_type = format_type_ref(arg["type"])
                    desc = (arg.get("description") or "").replace("\n", " ").replace("|", "\\|")
                    default = f" (default: `{arg['defaultValue']}`)" if arg.get("defaultValue") else ""
                    doc.append(f"| `{arg['name']}` | `{arg_type}` | {desc}{default} |\n")
                doc.append("\n")

    return "".join(doc)

def generate_enum_doc(enum_obj):
    """Generate documentation for an enum type."""
    doc = []
    doc.append(f"# {enum_obj['name']}\n\n")

    if enum_obj.get("description"):
        doc.append(f"{enum_obj['description']}\n\n")

    doc.append("**Kind:** ENUM\n\n")
    doc.append("## Values\n\n")
    doc.append("| Value | Description |\n")
    doc.append("|-------|-------------|\n")

    for val in (enum_obj.get("enumValues") or []):
        desc = (val.get("description") or "").replace("\n", " ").replace("|", "\\|")
        deprecated = " ⚠️ DEPRECATED" if val.get("isDeprecated") else ""
        doc.append(f"| `{val['name']}` | {desc}{deprecated} |\n")

    return "".join(doc)

def generate_input_doc(input_obj):
    """Generate documentation for an input type."""
    doc = []
    doc.append(f"# {input_obj['name']}\n\n")

    if input_obj.get("description"):
        doc.append(f"{input_obj['description']}\n\n")

    doc.append("**Kind:** INPUT_OBJECT\n\n")
    doc.append("## Fields\n\n")
    doc.append("| Field | Type | Required | Description |\n")
    doc.append("|-------|------|----------|-------------|\n")

    for field in (input_obj.get("inputFields") or []):
        field_type = format_type_ref(field["type"])
        required = "Yes" if field_type.endswith("!") else "No"
        desc = (field.get("description") or "").replace("\n", " ").replace("|", "\\|")
        default = f" (default: `{field['defaultValue']}`)" if field.get("defaultValue") else ""
        doc.append(f"| `{field['name']}` | `{field_type}` | {required} | {desc}{default} |\n")

    return "".join(doc)

def generate_union_doc(union_obj):
    """Generate documentation for a union type."""
    doc = []
    doc.append(f"# {union_obj['name']}\n\n")

    if union_obj.get("description"):
        doc.append(f"{union_obj['description']}\n\n")

    doc.append("**Kind:** UNION\n\n")
    doc.append("## Possible Types\n\n")

    for ptype in (union_obj.get("possibleTypes") or []):
        type_name = ptype.get("name", "Unknown")
        doc.append(f"- [{type_name}](./types/{type_name}.md)\n")

    return "".join(doc)

def generate_scalar_doc(scalar_obj):
    """Generate documentation for a scalar type."""
    doc = []
    doc.append(f"# {scalar_obj['name']}\n\n")

    if scalar_obj.get("description"):
        doc.append(f"{scalar_obj['description']}\n\n")

    doc.append("**Kind:** SCALAR\n\n")

    # Add common scalar descriptions
    scalar_info = {
        "String": "A UTF-8 character sequence.",
        "Int": "A signed 32-bit integer.",
        "Float": "A signed double-precision floating-point value.",
        "Boolean": "Represents `true` or `false`.",
        "ID": "A unique identifier, often used to refetch an object or as a cache key.",
        "AWSDateTime": "An extended ISO 8601 date and time string in the format YYYY-MM-DDThh:mm:ss.sssZ.",
        "AWSTimestamp": "An integer value representing the number of seconds before or after 1970-01-01-T00:00Z.",
        "AWSJSON": "A JSON string that complies with RFC 8259.",
        "AWSDate": "An extended ISO 8601 date string in the format YYYY-MM-DD.",
        "AWSTime": "An extended ISO 8601 time string in the format hh:mm:ss.sss.",
        "AWSEmail": "An email address string that complies with RFC 5321.",
        "AWSPhone": "A phone number string.",
        "AWSURL": "A URL string that complies with RFC 3986.",
    }

    if scalar_obj["name"] in scalar_info:
        doc.append(f"{scalar_info[scalar_obj['name']]}\n")

    return "".join(doc)

def generate_interface_doc(interface_obj):
    """Generate documentation for an interface type."""
    doc = []
    doc.append(f"# {interface_obj['name']}\n\n")

    if interface_obj.get("description"):
        doc.append(f"{interface_obj['description']}\n\n")

    doc.append("**Kind:** INTERFACE\n\n")

    if interface_obj.get("fields"):
        doc.append("## Fields\n\n")
        doc.append("| Field | Type | Description |\n")
        doc.append("|-------|------|-------------|\n")

        for field in interface_obj["fields"]:
            field_type = format_type_ref(field["type"])
            desc = (field.get("description") or "").replace("\n", " ").replace("|", "\\|")
            doc.append(f"| `{field['name']}` | `{field_type}` | {desc} |\n")

    if interface_obj.get("possibleTypes"):
        doc.append("\n## Implemented By\n\n")
        for ptype in interface_obj["possibleTypes"]:
            doc.append(f"- [{ptype['name']}](./types/{ptype['name']}.md)\n")

    return "".join(doc)

def generate_all_enums_doc(enums):
    """Generate a single document with all enums."""
    doc = []
    doc.append("# PGA Tour GraphQL API - Complete Enums Reference\n\n")
    doc.append(f"**Total Enums: {len(enums)}**\n\n")
    doc.append("---\n\n")
    doc.append("## Table of Contents\n\n")

    for enum in sorted(enums, key=lambda x: x["name"]):
        doc.append(f"- [{enum['name']}](#{enum['name'].lower()})\n")

    doc.append("\n---\n\n")

    for enum in sorted(enums, key=lambda x: x["name"]):
        doc.append(f"## {enum['name']}\n\n")

        if enum.get("description"):
            doc.append(f"{enum['description']}\n\n")

        doc.append("| Value | Description |\n")
        doc.append("|-------|-------------|\n")

        for val in (enum.get("enumValues") or []):
            desc = (val.get("description") or "").replace("\n", " ").replace("|", "\\|")
            deprecated = " ⚠️ DEPRECATED" if val.get("isDeprecated") else ""
            doc.append(f"| `{val['name']}` | {desc}{deprecated} |\n")

        doc.append("\n---\n\n")

    return "".join(doc)

def generate_all_types_doc(objects):
    """Generate a single document with all object types."""
    doc = []
    doc.append("# PGA Tour GraphQL API - Complete Object Types Reference\n\n")
    doc.append(f"**Total Object Types: {len(objects)}**\n\n")
    doc.append("---\n\n")
    doc.append("## Table of Contents\n\n")

    # Group by first letter
    by_letter = {}
    for obj in sorted(objects, key=lambda x: x["name"]):
        letter = obj["name"][0].upper()
        if letter not in by_letter:
            by_letter[letter] = []
        by_letter[letter].append(obj)

    for letter in sorted(by_letter.keys()):
        doc.append(f"### {letter}\n\n")
        for obj in by_letter[letter]:
            doc.append(f"- [{obj['name']}](#{obj['name'].lower()})\n")
        doc.append("\n")

    doc.append("\n---\n\n")

    for obj in sorted(objects, key=lambda x: x["name"]):
        doc.append(f"## {obj['name']}\n\n")

        if obj.get("description"):
            doc.append(f"{obj['description']}\n\n")

        if obj.get("interfaces"):
            interfaces = [i["name"] for i in obj["interfaces"] if i.get("name")]
            if interfaces:
                doc.append(f"**Implements:** {', '.join(interfaces)}\n\n")

        if obj.get("fields"):
            doc.append("### Fields\n\n")
            doc.append("| Field | Type | Description |\n")
            doc.append("|-------|------|-------------|\n")

            for field in obj["fields"]:
                field_type = format_type_ref(field["type"])
                desc = (field.get("description") or "").replace("\n", " ").replace("|", "\\|")[:100]
                deprecated = " ⚠️" if field.get("isDeprecated") else ""
                doc.append(f"| `{field['name']}` | `{field_type}` | {desc}{deprecated} |\n")

        doc.append("\n---\n\n")

    return "".join(doc)

def generate_all_inputs_doc(inputs):
    """Generate a single document with all input types."""
    doc = []
    doc.append("# PGA Tour GraphQL API - Complete Input Types Reference\n\n")
    doc.append(f"**Total Input Types: {len(inputs)}**\n\n")
    doc.append("---\n\n")

    for inp in sorted(inputs, key=lambda x: x["name"]):
        doc.append(f"## {inp['name']}\n\n")

        if inp.get("description"):
            doc.append(f"{inp['description']}\n\n")

        doc.append("### Fields\n\n")
        doc.append("| Field | Type | Required | Default | Description |\n")
        doc.append("|-------|------|----------|---------|-------------|\n")

        for field in (inp.get("inputFields") or []):
            field_type = format_type_ref(field["type"])
            required = "Yes" if field_type.endswith("!") else "No"
            desc = (field.get("description") or "").replace("\n", " ").replace("|", "\\|")
            default = f"`{field['defaultValue']}`" if field.get("defaultValue") else "-"
            doc.append(f"| `{field['name']}` | `{field_type}` | {required} | {default} | {desc} |\n")

        doc.append("\n---\n\n")

    return "".join(doc)

def generate_all_unions_doc(unions):
    """Generate a single document with all union types."""
    doc = []
    doc.append("# PGA Tour GraphQL API - Complete Union Types Reference\n\n")
    doc.append(f"**Total Union Types: {len(unions)}**\n\n")
    doc.append("---\n\n")

    for union in sorted(unions, key=lambda x: x["name"]):
        doc.append(f"## {union['name']}\n\n")

        if union.get("description"):
            doc.append(f"{union['description']}\n\n")

        doc.append("### Possible Types\n\n")
        for ptype in (union.get("possibleTypes") or []):
            doc.append(f"- `{ptype.get('name', 'Unknown')}`\n")

        doc.append("\n---\n\n")

    return "".join(doc)

def generate_scalars_doc(scalars):
    """Generate documentation for all scalar types."""
    doc = []
    doc.append("# PGA Tour GraphQL API - Scalar Types Reference\n\n")
    doc.append(f"**Total Scalar Types: {len(scalars)}**\n\n")
    doc.append("---\n\n")

    scalar_info = {
        "String": "A UTF-8 character sequence.",
        "Int": "A signed 32-bit integer.",
        "Float": "A signed double-precision floating-point value.",
        "Boolean": "Represents `true` or `false`.",
        "ID": "A unique identifier, often used to refetch an object or as a cache key.",
        "AWSDateTime": "An extended ISO 8601 date and time string in the format `YYYY-MM-DDThh:mm:ss.sssZ`.",
        "AWSTimestamp": "An integer value representing the number of seconds before or after `1970-01-01-T00:00Z`.",
        "AWSJSON": "A JSON string that complies with RFC 8259.",
        "AWSDate": "An extended ISO 8601 date string in the format `YYYY-MM-DD`.",
        "AWSTime": "An extended ISO 8601 time string in the format `hh:mm:ss.sss`.",
        "AWSEmail": "An email address string that complies with RFC 5321.",
        "AWSPhone": "A phone number string.",
        "AWSURL": "A URL string that complies with RFC 3986.",
    }

    for scalar in sorted(scalars, key=lambda x: x["name"]):
        doc.append(f"## {scalar['name']}\n\n")

        if scalar.get("description"):
            doc.append(f"{scalar['description']}\n\n")
        elif scalar["name"] in scalar_info:
            doc.append(f"{scalar_info[scalar['name']]}\n\n")

        doc.append("---\n\n")

    return "".join(doc)

def generate_interfaces_doc(interfaces):
    """Generate documentation for all interface types."""
    doc = []
    doc.append("# PGA Tour GraphQL API - Interface Types Reference\n\n")
    doc.append(f"**Total Interface Types: {len(interfaces)}**\n\n")
    doc.append("---\n\n")

    for iface in sorted(interfaces, key=lambda x: x["name"]):
        doc.append(f"## {iface['name']}\n\n")

        if iface.get("description"):
            doc.append(f"{iface['description']}\n\n")

        if iface.get("fields"):
            doc.append("### Fields\n\n")
            doc.append("| Field | Type | Description |\n")
            doc.append("|-------|------|-------------|\n")

            for field in iface["fields"]:
                field_type = format_type_ref(field["type"])
                desc = (field.get("description") or "").replace("\n", " ").replace("|", "\\|")
                doc.append(f"| `{field['name']}` | `{field_type}` | {desc} |\n")

        if iface.get("possibleTypes"):
            doc.append("\n### Implemented By\n\n")
            for ptype in iface["possibleTypes"]:
                doc.append(f"- `{ptype['name']}`\n")

        doc.append("\n---\n\n")

    return "".join(doc)

def generate_master_index(schema, stats):
    """Generate the master index document."""
    doc = []
    doc.append("# PGA Tour GraphQL API - Complete Schema Reference\n\n")
    doc.append("**Auto-generated via GraphQL Introspection**\n\n")
    doc.append("---\n\n")

    doc.append("## Schema Statistics\n\n")
    doc.append("| Category | Count |\n")
    doc.append("|----------|-------|\n")
    doc.append(f"| Queries | {stats['queries']} |\n")
    doc.append(f"| Mutations | {stats['mutations']} |\n")
    doc.append(f"| Object Types | {stats['objects']} |\n")
    doc.append(f"| Enum Types | {stats['enums']} |\n")
    doc.append(f"| Input Types | {stats['inputs']} |\n")
    doc.append(f"| Union Types | {stats['unions']} |\n")
    doc.append(f"| Scalar Types | {stats['scalars']} |\n")
    doc.append(f"| Interface Types | {stats['interfaces']} |\n")
    doc.append(f"| **Total** | **{sum(stats.values())}** |\n\n")

    doc.append("---\n\n")

    doc.append("## Documentation Files\n\n")
    doc.append("| File | Description |\n")
    doc.append("|------|-------------|\n")
    doc.append("| [queries.md](./docs/queries.md) | Complete reference for all 193 queries |\n")
    doc.append("| [mutations.md](./docs/mutations.md) | Complete reference for all 64 mutations |\n")
    doc.append("| [types.md](./docs/types.md) | Complete reference for all 747 object types |\n")
    doc.append("| [enums.md](./docs/enums.md) | Complete reference for all 94 enum types |\n")
    doc.append("| [inputs.md](./docs/inputs.md) | Complete reference for all 8 input types |\n")
    doc.append("| [unions.md](./docs/unions.md) | Complete reference for all 45 union types |\n")
    doc.append("| [scalars.md](./docs/scalars.md) | Complete reference for all scalar types |\n")
    doc.append("| [interfaces.md](./docs/interfaces.md) | Complete reference for all interface types |\n\n")

    doc.append("---\n\n")

    doc.append("## API Endpoint\n\n")
    doc.append("```\n")
    doc.append("URL: https://orchestrator.pgatour.com/graphql\n")
    doc.append("Method: POST\n")
    doc.append("Headers:\n")
    doc.append("  x-api-key: <your-api-key>\n")
    doc.append("  x-pgat-platform: web\n")
    doc.append("  Content-Type: application/json\n")
    doc.append("```\n\n")

    doc.append("---\n\n")

    doc.append("## Tour Codes\n\n")
    doc.append("| Code | Tour |\n")
    doc.append("|------|------|\n")
    doc.append("| `R` | PGA TOUR (Regular) |\n")
    doc.append("| `H` | Champions Tour |\n")
    doc.append("| `M` | Korn Ferry Tour |\n")
    doc.append("| `S` | PGA TOUR Americas |\n")
    doc.append("| `C` | PGA TOUR Canada |\n")
    doc.append("| `I` | International Tours |\n")
    doc.append("| `Y` | Youth/College |\n")
    doc.append("| `U` | University |\n")
    doc.append("| `E` | DP World Tour (European) |\n\n")

    return "".join(doc)

def main():
    print("Loading schema...")
    schema = load_schema()

    types = schema.get("types", [])
    custom_types = [t for t in types if not t["name"].startswith("__")]

    # Categorize types
    objects = [t for t in custom_types if t["kind"] == "OBJECT" and t["name"] not in ["Query", "Mutation", "Subscription"]]
    enums = [t for t in custom_types if t["kind"] == "ENUM"]
    inputs = [t for t in custom_types if t["kind"] == "INPUT_OBJECT"]
    unions = [t for t in custom_types if t["kind"] == "UNION"]
    scalars = [t for t in custom_types if t["kind"] == "SCALAR"]
    interfaces = [t for t in custom_types if t["kind"] == "INTERFACE"]

    # Get query/mutation counts
    query_type = next((t for t in types if t["name"] == schema.get("queryType", {}).get("name")), None)
    mutation_type = next((t for t in types if t["name"] == schema.get("mutationType", {}).get("name")), None)

    stats = {
        "queries": len(query_type.get("fields", [])) if query_type else 0,
        "mutations": len(mutation_type.get("fields", [])) if mutation_type else 0,
        "objects": len(objects),
        "enums": len(enums),
        "inputs": len(inputs),
        "unions": len(unions),
        "scalars": len(scalars),
        "interfaces": len(interfaces),
    }

    # Create docs directory
    os.makedirs("docs", exist_ok=True)

    # Generate all documentation
    print(f"Generating queries documentation ({stats['queries']} queries)...")
    with open("docs/queries.md", "w") as f:
        f.write(generate_queries_doc(schema))

    print(f"Generating mutations documentation ({stats['mutations']} mutations)...")
    with open("docs/mutations.md", "w") as f:
        f.write(generate_mutations_doc(schema))

    print(f"Generating object types documentation ({stats['objects']} types)...")
    with open("docs/types.md", "w") as f:
        f.write(generate_all_types_doc(objects))

    print(f"Generating enum types documentation ({stats['enums']} enums)...")
    with open("docs/enums.md", "w") as f:
        f.write(generate_all_enums_doc(enums))

    print(f"Generating input types documentation ({stats['inputs']} inputs)...")
    with open("docs/inputs.md", "w") as f:
        f.write(generate_all_inputs_doc(inputs))

    print(f"Generating union types documentation ({stats['unions']} unions)...")
    with open("docs/unions.md", "w") as f:
        f.write(generate_all_unions_doc(unions))

    print(f"Generating scalar types documentation ({stats['scalars']} scalars)...")
    with open("docs/scalars.md", "w") as f:
        f.write(generate_scalars_doc(scalars))

    print(f"Generating interface types documentation ({stats['interfaces']} interfaces)...")
    with open("docs/interfaces.md", "w") as f:
        f.write(generate_interfaces_doc(interfaces))

    print("Generating master index...")
    with open("docs/README.md", "w") as f:
        f.write(generate_master_index(schema, stats))

    print("\n" + "=" * 60)
    print("DOCUMENTATION GENERATION COMPLETE")
    print("=" * 60)
    print(f"\nGenerated files in ./docs/:")
    print(f"  - README.md (Master Index)")
    print(f"  - queries.md ({stats['queries']} queries)")
    print(f"  - mutations.md ({stats['mutations']} mutations)")
    print(f"  - types.md ({stats['objects']} object types)")
    print(f"  - enums.md ({stats['enums']} enum types)")
    print(f"  - inputs.md ({stats['inputs']} input types)")
    print(f"  - unions.md ({stats['unions']} union types)")
    print(f"  - scalars.md ({stats['scalars']} scalar types)")
    print(f"  - interfaces.md ({stats['interfaces']} interface types)")
    print(f"\nTotal coverage: {sum(stats.values())} schema elements")

if __name__ == "__main__":
    main()
