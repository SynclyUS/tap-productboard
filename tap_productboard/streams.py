from tap_productboard.client import ProductboardStream


class CompaniesStream(ProductboardStream):
    name = "companies"
    path = "/companies"
    primary_keys = ["id"]


class ComponentsStream(ProductboardStream):
    name = "components"
    path = "/components"
    primary_keys = ["id"]


class FeaturesStream(ProductboardStream):
    name = "features"
    path = "/features"
    primary_keys = ["id"]


# Initiatives are not enabled in all spaces
class InitiativesStream(ProductboardStream):
    name = "initiatives"
    path = "/initiatives"
    primary_keys = ["id"]


# Key results are not enabled in all spaces
class KeyResultsStream(ProductboardStream):
    name = "key_results"
    path = "/key-results"
    primary_keys = ["id"]


class NotesStream(ProductboardStream):
    name = "notes"
    path = "/notes"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    replication_param = "updatedFrom"
    next_page_token_jsonpath = "$.pageCursor"


class ObjectivesStream(ProductboardStream):
    name = "objectives"
    path = "/objectives"
    primary_keys = ["id"]


class ProductsStream(ProductboardStream):
    name = "products"
    path = "/products"
    primary_keys = ["id"]


class ReleasesStream(ProductboardStream):
    name = "releases"
    path = "/releases"
    primary_keys = ["id"]


class ReleaseGroupsStream(ProductboardStream):
    name = "release_groups"
    path = "/release-groups"
    primary_keys = ["id"]


class UsersStream(ProductboardStream):
    name = "users"
    path = "/users"
    primary_keys = ["id"]
