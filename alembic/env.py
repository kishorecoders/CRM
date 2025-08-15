from logging.config import fileConfig

from alembic import context
from src.config import get_settings

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlmodel import SQLModel 

from src.Category import models
from src.Integration import models
from src.Activity import models
from src.AdminAddEmployee import models
from src.AdminAssignRoleEmployee import models
from src.AdminRoleCreation import models
from src.AdminSales import models
from src.Inventoryoutward import models
from src.Invoice import models
from src.Leads import models
from src.Meetingplanned import models
from src.Ocr import models
from src.Productwisestock import models
from src.ProjectManagerOrder import models
from src.PurchaseManager import models
from src.PurchaseOrderIssue import models
from src.Quotation import models
from src.Settings import models
from src.SettingsFiles import models
from src.StoreManagerProduct import models
from src.StoreManagerPurchase import models
from src.StoreManagerService import models
from src.SubCategory import models
from src.SuperAdminBilling import models
from src.SuperAdminEnquiry import models
from src.SuperAdminPlanAndPrice import models
from src.SuperAdminReffralAndPlan import models
from src.SuperAdminUserAddNew import models
from src.vendor import models
from src.EmployeeAssignRequest import models
from src.EmployeeFiles import models
from src.EmployeeTasks import models
from src.Attendance import models
from src.RoleAssignByLevel import models
from src.TimeConfig import models
from src.ActivityComment import models
from src.EmployeeLeave import models
from src.PublicHoliday import models
from src.QuotationTemplate import models
from src.QuotationProduct import models
from src.QuotationProductEmployee import models
from src.TermAndConditions import models
from src.Brouncher import models
from src.Production import models
from src.ProductionRequest import models
from src.LeadReminder import models
from src.DispatchVendor import models
from src.CreateDispatch import models
from src.DeliveryChallan import models
from src.ProductStages import models
from src.ProductSteps import models
from src.StepItems import models
from src.LateMark import models
from src.DesignHandover import models
from src.QuotationCustomer import models
from src.QuotationSeries import models
from src.Bank import models
from src.PaymentTerm import models
from src.Account import models
from src.ProductDispatch import models
from src.AddPayment import models
from src.PiValue import models
from src.TermAndConditionContent import models
from src.QuotationSubProductEmployee import models
from src.CheckPoint import models
from src.ProductTemplates import models
from src.ProjectManagerResourseFile import models

from src.ProductTemplates_key import models
from src.StoreSubProductEmployee import models
from src.StoreCheckPoint import models
from src.StoreTemplates import models
from src.Quotation_stages import models

from src.PurchaseOrderProduct import models

from src.StoreProductTemplates_key import models

from src.FaceBook import models
from src.CreateDispatchInfo import models
from src.InventoryOutwardRemark import models
from src.EmployeeTasksCustomer import models
from src.ProductQuantityDetails import models
from src.AdminAssignRoleDetail import models
from src.AssignRequestRemark import models
from src.TasksStatusHistory import models
from src.GrnOrders import models
from src.GrnOrderProduct import models
from src.GrnInvoice import models
from src.Rfq import models
from src.Subscribe import models
from src.SubscribeOtp import models
from src.ProjectTasks import models  
from src.Notifications import models
from src.NotificationsReadStatus import models
from src.EmployeeTasksMessage import models
from src.DailyTaskReport import models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config

settings = get_settings()

config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URI)


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
