import climmob.plugins as plugins
import climmob.plugins.utilities as u
from climmob.products.climmob_products import (
    createProductDirectory,
    registerProductInstance,
)
from dataCollectionProgressExtension.celerytasks import createDataCollectionProgress


class dataCollectionProgressExtension(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfig)
    # plugins.implements(plugins.IProduct)
    plugins.implements(plugins.IDataColletionProgress)

    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.addTemplatesDirectory(config, "templates")

    # def register_products(self, config):
    #     # DATA COLLECTION PROGRESS
    #
    #     # datacollectionprogressProduct = addProduct(
    #     #     "datacollectionprogress",
    #     #     "Shows the information of the observers from whom the information has been collected",
    #     # )
    #     # addMetadataToProduct(datacollectionprogressProduct, "author", "Brandon Madriz")
    #     # addMetadataToProduct(datacollectionprogressProduct, "version", "1.0")
    #     # addMetadataToProduct(
    #     #     datacollectionprogressProduct,
    #     #     "Licence",
    #     #     "Copyright 2020, Alliance of Bioversity International and CIAT",
    #     # )
    #     # products.append(datacollectionprogressProduct)
    #
    #     productInformation = [
    #         {
    #             "name": "datacollectionprogress",
    #             "description": "Shows the information of the observers from whom the information has been collected",
    #             "metadata": {
    #                 "author": "Brandon Madriz",
    #                 "version": "1.0",
    #                 "Licence": "Copyright 2022, MrBot Software Solutions",
    #             },
    #         }
    #     ]
    #     return productInformation

    def create_data_collection_progress(
        self,
        request,
        locale,
        userOwner,
        projectId,
        projectCod,
        projectDetails,
        geoInformation,
    ):
        # We create the plugin directory if it does not exists and return it
        # The path user.repository in development.ini/user/project/products/product and
        # user.repository in development.ini/user/project/products/product/outputs
        path = createProductDirectory(
            request, userOwner, projectCod, "datacollectionprogress"
        )
        # We call the Celery task that will generate the output packages.pdf
        task = createDataCollectionProgress.apply_async(
            (locale, userOwner, path, projectCod, projectDetails, geoInformation),
            queue="ClimMob",
        )
        # We register the instance of the output with the task ID of celery
        # This will go to the products table that then you can monitor and use
        # in the nice product interface

        registerProductInstance(
            projectId,
            "datacollectionprogress",
            "datacollectionprogress_" + projectCod + ".docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "create_data_collection_progress",
            task.id,
            request,
        )
