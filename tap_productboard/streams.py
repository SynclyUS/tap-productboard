from tap_productboard.client import ProductboardStream


class CompaniesStream(ProductboardStream):
    name = "companies"
    path = "/companies"


class ComponentsStream(ProductboardStream):
    name = "components"
    path = "/components"


class FeaturesStream(ProductboardStream):
    name = "features"
    path = "/features"


# Initiatives are not enabled in all spaces
class InitiativesStream(ProductboardStream):
    name = "initiatives"
    path = "/initiatives"


# Key results are not enabled in all spaces
class KeyResultsStream(ProductboardStream):
    name = "key_results"
    path = "/key-results"


class NotesStream(ProductboardStream):
    name = "notes"
    path = "/notes"
    replication_key = "updatedAt"
    replication_param = "updatedFrom"
    next_page_token_jsonpath = "$.pageCursor"


class ObjectivesStream(ProductboardStream):
    name = "objectives"
    path = "/objectives"


class ProductsStream(ProductboardStream):
    name = "products"
    path = "/products"


class ReleasesStream(ProductboardStream):
    name = "releases"
    path = "/releases"


class ReleaseGroupsStream(ProductboardStream):
    name = "release_groups"
    path = "/release-groups"


class UsersStream(ProductboardStream):
    name = "users"
    path = "/users"
