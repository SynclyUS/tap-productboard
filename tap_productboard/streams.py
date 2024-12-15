from tap_productboard.client import ProductboardStream


class CompaniesStream(ProductboardStream):
    """
    Companies stream
    https://developer.productboard.com/reference/getcompanies-1
    """

    name = "companies"
    path = "/companies"


class ComponentsStream(ProductboardStream):
    """
    Components stream
    https://developer.productboard.com/reference/getcomponents-1
    """

    name = "components"
    path = "/components"


class FeaturesStream(ProductboardStream):
    """
    Features stream
    https://developer.productboard.com/reference/getfeatures-1
    """

    name = "features"
    path = "/features"


class InitiativesStream(ProductboardStream):
    """
    Initiatives stream, not enabled as not all spaces have initiatives
    https://developer.productboard.com/reference/getinitiatives
    """

    name = "initiatives"
    path = "/initiatives"


class KeyResultsStream(ProductboardStream):
    """
    Key results stream, not enabled as not all spaces have key results
    https://developer.productboard.com/reference/getkeyresults
    """

    name = "key_results"
    path = "/key-results"


class NotesStream(ProductboardStream):
    """
    Notes stream
    https://developer.productboard.com/reference/getnotes-1

    Replication key and param are included to enable incremental replication.
    The notes endpoint also uses a different pagination method from the other endpoints.
    """

    name = "notes"
    path = "/notes"
    replication_key = "updatedAt"
    replication_param = "updatedFrom"
    next_page_token_jsonpath = "$.pageCursor"


class ObjectivesStream(ProductboardStream):
    """
    Objectives stream
    https://developer.productboard.com/reference/getobjectives-1
    """

    name = "objectives"
    path = "/objectives"


class ProductsStream(ProductboardStream):
    """
    Products stream
    https://developer.productboard.com/reference/getproducts-1
    """

    name = "products"
    path = "/products"


class ReleaseGroupsStream(ProductboardStream):
    """
    Release groups stream
    https://developer.productboard.com/reference/listreleasegroups-1
    """

    name = "release_groups"
    path = "/release-groups"


class ReleasesStream(ProductboardStream):
    """
    Releases stream
    https://developer.productboard.com/reference/listreleases-1
    """

    name = "releases"
    path = "/releases"


class UsersStream(ProductboardStream):
    """
    Users stream
    https://developer.productboard.com/reference/getusers-1
    """

    name = "users"
    path = "/users"
