#!/usr/bin/env python3
"""
PGA Tour GraphQL API Introspection Script
Maps out the complete GraphQL schema using introspection queries.
"""

import os
import json
import requests
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().strip().split("\n"):
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def introspect_schema():
    """Fetch the complete GraphQL schema using introspection."""
    url = "https://orchestrator.pgatour.com/graphql"
    headers = {
        "x-api-key": os.getenv("PGA_TOUR_API_KEY"),
        "x-pgat-platform": "web"
    }

    # Standard GraphQL introspection query
    introspection_query = {
        "query": """
            query IntrospectionQuery {
              __schema {
                queryType { name }
                mutationType { name }
                subscriptionType { name }
                types {
                  ...FullType
                }
                directives {
                  name
                  description
                  locations
                  args {
                    ...InputValue
                  }
                }
              }
            }

            fragment FullType on __Type {
              kind
              name
              description
              fields(includeDeprecated: true) {
                name
                description
                args {
                  ...InputValue
                }
                type {
                  ...TypeRef
                }
                isDeprecated
                deprecationReason
              }
              inputFields {
                ...InputValue
              }
              interfaces {
                ...TypeRef
              }
              enumValues(includeDeprecated: true) {
                name
                description
                isDeprecated
                deprecationReason
              }
              possibleTypes {
                ...TypeRef
              }
            }

            fragment InputValue on __InputValue {
              name
              description
              type {
                ...TypeRef
              }
              defaultValue
            }

            fragment TypeRef on __Type {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                    ofType {
                      kind
                      name
                      ofType {
                        kind
                        name
                        ofType {
                          kind
                          name
                          ofType {
                            kind
                            name
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
        """
    }

    print("Sending introspection query to PGA Tour API...")
    print(f"API Key present: {bool(os.getenv('PGA_TOUR_API_KEY'))}")

    try:
        response = requests.post(url, json=introspection_query, headers=headers)
        response.raise_for_status()
        json_response = response.json()

        if "errors" in json_response:
            print("GraphQL Errors:")
            print(json.dumps(json_response["errors"], indent=2))
            return None

        if "data" in json_response and "__schema" in json_response["data"]:
            return json_response["data"]["__schema"]
        else:
            print("Unexpected response structure:")
            print(json.dumps(json_response, indent=2)[:2000])
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text[:1000]}")
        return None


def format_type_ref(type_ref):
    """Format a type reference into a readable string."""
    if type_ref is None:
        return "Unknown"

    kind = type_ref.get("kind")
    name = type_ref.get("name")
    of_type = type_ref.get("ofType")

    if kind == "NON_NULL":
        return f"{format_type_ref(of_type)}!"
    elif kind == "LIST":
        return f"[{format_type_ref(of_type)}]"
    elif name:
        return name
    else:
        return "Unknown"


def analyze_schema(schema):
    """Analyze and summarize the schema."""
    print("\n" + "=" * 80)
    print("PGA TOUR GRAPHQL API SCHEMA ANALYSIS")
    print("=" * 80)

    # Root types
    print("\n## Root Types")
    print(f"- Query Type: {schema.get('queryType', {}).get('name', 'None')}")
    print(f"- Mutation Type: {schema.get('mutationType', {}).get('name', 'None')}")
    print(f"- Subscription Type: {schema.get('subscriptionType', {}).get('name', 'None')}")

    # Categorize types
    types = schema.get("types", [])

    # Filter out built-in types (those starting with __)
    custom_types = [t for t in types if not t["name"].startswith("__")]
    builtin_types = [t for t in types if t["name"].startswith("__")]

    # Categorize by kind
    objects = [t for t in custom_types if t["kind"] == "OBJECT"]
    inputs = [t for t in custom_types if t["kind"] == "INPUT_OBJECT"]
    enums = [t for t in custom_types if t["kind"] == "ENUM"]
    scalars = [t for t in custom_types if t["kind"] == "SCALAR"]
    interfaces = [t for t in custom_types if t["kind"] == "INTERFACE"]
    unions = [t for t in custom_types if t["kind"] == "UNION"]

    print(f"\n## Type Statistics")
    print(f"- Object Types: {len(objects)}")
    print(f"- Input Types: {len(inputs)}")
    print(f"- Enum Types: {len(enums)}")
    print(f"- Scalar Types: {len(scalars)}")
    print(f"- Interface Types: {len(interfaces)}")
    print(f"- Union Types: {len(unions)}")
    print(f"- Built-in Types: {len(builtin_types)}")

    # Find Query type and list all queries
    query_type = next((t for t in types if t["name"] == schema.get('queryType', {}).get('name')), None)
    if query_type and query_type.get("fields"):
        print(f"\n## Available Queries ({len(query_type['fields'])} total)")
        print("-" * 40)
        for field in sorted(query_type["fields"], key=lambda x: x["name"]):
            args_str = ""
            if field.get("args"):
                args_list = [f"{a['name']}: {format_type_ref(a['type'])}" for a in field["args"]]
                args_str = f"({', '.join(args_list)})"
            return_type = format_type_ref(field.get("type"))
            print(f"  {field['name']}{args_str}: {return_type}")
            if field.get("description"):
                print(f"    # {field['description'][:100]}")

    # Find Mutation type
    mutation_type = next((t for t in types if t["name"] == schema.get('mutationType', {}).get('name')), None)
    if mutation_type and mutation_type.get("fields"):
        print(f"\n## Available Mutations ({len(mutation_type['fields'])} total)")
        print("-" * 40)
        for field in sorted(mutation_type["fields"], key=lambda x: x["name"]):
            args_str = ""
            if field.get("args"):
                args_list = [f"{a['name']}: {format_type_ref(a['type'])}" for a in field["args"]]
                args_str = f"({', '.join(args_list)})"
            return_type = format_type_ref(field.get("type"))
            print(f"  {field['name']}{args_str}: {return_type}")

    # List all enums
    if enums:
        print(f"\n## Enum Types ({len(enums)} total)")
        print("-" * 40)
        for enum in sorted(enums, key=lambda x: x["name"]):
            values = [v["name"] for v in (enum.get("enumValues") or [])]
            print(f"  {enum['name']}: {', '.join(values)}")

    # List key object types (non-root types with fields)
    print(f"\n## Object Types ({len(objects)} total)")
    print("-" * 40)
    for obj in sorted(objects, key=lambda x: x["name"]):
        if obj["name"] not in ["Query", "Mutation", "Subscription"]:
            field_count = len(obj.get("fields") or [])
            print(f"  {obj['name']} ({field_count} fields)")

    return {
        "queries": query_type.get("fields") if query_type else [],
        "mutations": mutation_type.get("fields") if mutation_type else [],
        "objects": objects,
        "enums": enums,
        "inputs": inputs,
        "scalars": scalars,
        "interfaces": interfaces,
        "unions": unions
    }


def save_detailed_schema(schema, analysis):
    """Save detailed schema documentation to files."""

    # Determine output paths based on where script is run from
    schema_dir = "../schema" if os.path.exists("../schema") else "schema"
    os.makedirs(schema_dir, exist_ok=True)

    # Save raw schema
    schema_path = os.path.join(schema_dir, "schema.json")
    with open(schema_path, "w") as f:
        json.dump(schema, f, indent=2)
    print(f"\nSaved raw schema to: {schema_path}")

    # Create detailed documentation
    doc = []
    doc.append("# PGA Tour GraphQL API Schema Documentation\n")
    doc.append("Auto-generated via introspection\n\n")

    # Queries section
    if analysis["queries"]:
        doc.append("## Queries\n\n")
        for field in sorted(analysis["queries"], key=lambda x: x["name"]):
            doc.append(f"### {field['name']}\n\n")
            if field.get("description"):
                doc.append(f"{field['description']}\n\n")

            if field.get("args"):
                doc.append("**Arguments:**\n")
                for arg in field["args"]:
                    arg_type = format_type_ref(arg["type"])
                    default = f" = {arg['defaultValue']}" if arg.get("defaultValue") else ""
                    desc = f" - {arg['description']}" if arg.get("description") else ""
                    doc.append(f"- `{arg['name']}`: `{arg_type}`{default}{desc}\n")
                doc.append("\n")

            doc.append(f"**Returns:** `{format_type_ref(field['type'])}`\n\n")
            doc.append("---\n\n")

    # Object types section
    if analysis["objects"]:
        doc.append("## Object Types\n\n")
        for obj in sorted(analysis["objects"], key=lambda x: x["name"]):
            if obj["name"] in ["Query", "Mutation", "Subscription"]:
                continue
            doc.append(f"### {obj['name']}\n\n")
            if obj.get("description"):
                doc.append(f"{obj['description']}\n\n")

            if obj.get("fields"):
                doc.append("**Fields:**\n")
                for field in obj["fields"]:
                    field_type = format_type_ref(field["type"])
                    desc = f" - {field['description']}" if field.get("description") else ""
                    deprecated = " (DEPRECATED)" if field.get("isDeprecated") else ""
                    doc.append(f"- `{field['name']}`: `{field_type}`{deprecated}{desc}\n")
                doc.append("\n")
            doc.append("---\n\n")

    # Enum types section
    if analysis["enums"]:
        doc.append("## Enum Types\n\n")
        for enum in sorted(analysis["enums"], key=lambda x: x["name"]):
            doc.append(f"### {enum['name']}\n\n")
            if enum.get("description"):
                doc.append(f"{enum['description']}\n\n")

            if enum.get("enumValues"):
                doc.append("**Values:**\n")
                for val in enum["enumValues"]:
                    desc = f" - {val['description']}" if val.get("description") else ""
                    deprecated = " (DEPRECATED)" if val.get("isDeprecated") else ""
                    doc.append(f"- `{val['name']}`{deprecated}{desc}\n")
                doc.append("\n")
            doc.append("---\n\n")

    # Input types section
    if analysis["inputs"]:
        doc.append("## Input Types\n\n")
        for inp in sorted(analysis["inputs"], key=lambda x: x["name"]):
            doc.append(f"### {inp['name']}\n\n")
            if inp.get("description"):
                doc.append(f"{inp['description']}\n\n")

            if inp.get("inputFields"):
                doc.append("**Fields:**\n")
                for field in inp["inputFields"]:
                    field_type = format_type_ref(field["type"])
                    default = f" = {field['defaultValue']}" if field.get("defaultValue") else ""
                    desc = f" - {field['description']}" if field.get("description") else ""
                    doc.append(f"- `{field['name']}`: `{field_type}`{default}{desc}\n")
                doc.append("\n")
            doc.append("---\n\n")

    # Note: Full documentation is generated by generate_docs.py
    print("\nRun 'python scripts/generate_docs.py' to generate full documentation.")


if __name__ == "__main__":
    schema = introspect_schema()
    if schema:
        analysis = analyze_schema(schema)
        save_detailed_schema(schema, analysis)
        print("\n" + "=" * 80)
        print("Introspection complete!")
        print("=" * 80)
    else:
        print("\nIntrospection failed. The API may have introspection disabled.")
        print("Alternative: We can explore the API by testing known queries.")
