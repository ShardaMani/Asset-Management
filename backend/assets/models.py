# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Building(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)
    # original column f_seyv68l9ed8 - treat as building name/code
    name = models.CharField(db_column='f_seyv68l9ed8', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_41st5dm87n6'

    def __str__(self):
        return self.name or f"Building {self.id}"


class Room(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)
    room_code = models.CharField(db_column='f_6up8tma4yb5', max_length=255, unique=True, blank=True, null=True)
    # f_z5btgsashyb looks like a numeric pointer — link to Building if that's the case
    building = models.ForeignKey(Building, db_column='f_z5btgsashyb', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        managed = False
        db_table = 't_2dtcqclj5ht'

    def __str__(self):
        return self.room_code or f"Room {self.id}"



class SRB(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)
    srb_date = models.DateField(db_column='f_e2nmi66e869', blank=True, null=True)
    srb_number = models.CharField(db_column='f_g0e9afuz3v7', max_length=255, unique=True, blank=True, null=True)
    # f_lxjwdvg691h could be linked to an asset id (keep raw)
    related_id = models.BigIntegerField(db_column='f_lxjwdvg691h', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_3aer8zsk1up'

    def __str__(self):
        return self.srb_number or f"SRB {self.id}"



class AssetCategory(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)
    code = models.CharField(db_column='f_2cgnk4421ua', max_length=255, unique=True, blank=True, null=True)
    extra = models.TextField(db_column='f_m0dfxe8sg39', blank=True, null=True)
    name = models.CharField(db_column='f_ll176aoqwta', max_length=255, blank=True, null=True)
    description = models.TextField(db_column='Description', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_z3av1u74nej'

    def __str__(self):
        return self.name or self.code or f"Category {self.id}"

class AssetModel(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)
    model_name = models.CharField(db_column='f_zdb8nccxni1', max_length=255, blank=True, null=True)
    extra_info = models.TextField(db_column='f_410gngkfyi3', blank=True, null=True)
    # foreign key to AssetCategory (inspectdb showed asset_category_id)
    asset_category = models.ForeignKey(AssetCategory, db_column='Asset_Category_ID', null=True, blank=True, on_delete=models.SET_NULL)
    attributes = models.JSONField(db_column='f_cutof07n9os', blank=True, null=True)
    # building linkage if present
    building = models.ForeignKey(Building, db_column='Building_ID', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(db_column='Description', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_jjjq71q1d0b'

    def __str__(self):
        return self.model_name or f"Model {self.id}"



class AssetInstance(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)
    tag = models.CharField(db_column='f_tc2yj5sppje', max_length=255, unique=True, blank=True, null=True)
    label = models.CharField(db_column='f_4lanr254fp8', max_length=255, blank=True, null=True)
    is_active = models.BooleanField(db_column='f_l6a3ptwd2mg', blank=True, null=True)
    # FK to AssetModel (inspectdb column asset_model_Id)
    asset_model = models.ForeignKey(AssetModel, db_column='asset_model_Id', null=True, blank=True, on_delete=models.SET_NULL)
    # Room column was 'Room' (keep as FK to Room)
    room = models.ForeignKey(Room, db_column='Room', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(db_column='Description', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_vodrjekfz5h'

    def __str__(self):
        return self.tag or self.label or f"Instance {self.id}"

class AssetAcquisition(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)  # Field name made lowercase.
    srb_date = models.DateField(blank=True, null=True)
    purchase_order_number = models.CharField(max_length=255, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)
    funding_source = models.CharField(max_length=255, blank=True, null=True)
    budget = models.BigIntegerField(blank=True, null=True)
    purchase_amount = models.BigIntegerField(db_column='Purchase_amount', blank=True, null=True)  # Field name made lowercase.
    discount = models.BigIntegerField(blank=True, null=True)
    tax = models.BigIntegerField(blank=True, null=True)
    f_x666ook0x5c = models.BigIntegerField(blank=True, null=True)
    f_e2jp7hbx13o = models.BigIntegerField(blank=True, null=True)
    f_iprfru737sd = models.BigAutoField(primary_key=True)
    asset_id = models.BigIntegerField(db_column='Asset_id', blank=True, null=True)  # Field name made lowercase.
    f_d9zluekkg70 = models.CharField(max_length=255, blank=True, null=True)
    srb_number = models.BigIntegerField(blank=True, null=True)
    end_user_id = models.CharField(max_length=255, blank=True, null=True)
    procurement_authority_id = models.CharField(db_column='Procurement_Authority_Id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vendor_id = models.CharField(db_column='Vendor_Id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AssetAcquisition'


class Assetcondition(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)  # Field name made lowercase.
    status_of_asset = models.CharField(db_column='Status_of_asset', max_length=255, blank=True, null=True)  # Field name made lowercase.
    expected_lifetime = models.BigIntegerField(blank=True, null=True)
    utilization_frequency = models.CharField(max_length=255, blank=True, null=True)
    hazardous_classification = models.BooleanField(blank=True, null=True)
    f_gs4ymyolzuq = models.BigIntegerField(blank=True, null=True)
    f_n56m8iwg0sk = models.BigIntegerField(blank=True, null=True)
    f_rxxatzt6x8c = models.BigIntegerField(blank=True, null=True)
    f_xz9xpg0pqek = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'AssetCondition'


class Assetcoveragehistory(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)  # Field name made lowercase.
    f_2f6s2821arg = models.BigIntegerField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    type_of_coverage = models.CharField(max_length=255, blank=True, null=True)
    f_5prbf533wsd = models.BigIntegerField(blank=True, null=True)
    f_msddvfveplx = models.BigIntegerField(blank=True, null=True)
    f_egneb61jq45 = models.BigAutoField(primary_key=True)
    f_q6l42vct4hb = models.DateTimeField(blank=True, null=True)
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AssetCoverageHistory'


class Assetmovement(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)  # Field name made lowercase.
    current_status = models.CharField(db_column='Current_status', max_length=255, blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    geo_coordinates_of_destination = models.TextField(db_column='Geo_coordinates_of_destination', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    geo_coordinates_of_start_location = models.TextField(db_column='Geo_coordinates_of_start_location', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    f_nmwxy2znmt3 = models.BigIntegerField(blank=True, null=True)
    f_qv5vnwacf00 = models.BigIntegerField(blank=True, null=True)
    f_pmm6jhjavv1 = models.BigIntegerField(blank=True, null=True)
    f_11fgkbnf7dl = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'AssetMovement'


class Assetspecs(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)  # Field name made lowercase.
    is_power_required = models.BooleanField(db_column='Is_power_required', blank=True, null=True)  # Field name made lowercase.
    number_of_power_sources = models.BigIntegerField(db_column='Number_of_power_sources', blank=True, null=True)  # Field name made lowercase.
    power_requirement = models.BigIntegerField(blank=True, null=True)
    f_j8fbkt05op7 = models.BigIntegerField(blank=True, null=True)
    f_2iwml5sl5wc = models.BigIntegerField(blank=True, null=True)
    f_7k9wqrl450i = models.BigIntegerField(blank=True, null=True)
    f_wfvanzit9k0 = models.BigAutoField(primary_key=True)
    f_1fmjop02pa3 = models.CharField(max_length=255, blank=True, null=True)
    f_n1fl3v63c8i = models.BigIntegerField(blank=True, null=True)
    f_boh62iafj91 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AssetSpecs'


class Assetverificationlog(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)  # Field name made lowercase.
    f_kamhomozmbr = models.BigIntegerField(blank=True, null=True)
    verification_date = models.DateField(blank=True, null=True)
    location_of_verification = models.TextField(blank=True, null=True)  # This field type is a guess.
    f_1hkbnhi6emt = models.BigIntegerField(blank=True, null=True)
    f_hj6757uj171 = models.BigIntegerField(blank=True, null=True)
    f_seqpstreulq = models.BigAutoField(primary_key=True)
    f_gm0anvuak1m = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'AssetVerificationLog'


class Attacheddocument(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    createdbyid = models.BigIntegerField(db_column='createdById', blank=True, null=True)  # Field name made lowercase.
    updatedbyid = models.BigIntegerField(db_column='updatedById', blank=True, null=True)  # Field name made lowercase.
    document_type = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    f_0s7tsdefjv9 = models.BigIntegerField(blank=True, null=True)
    f_oby6pue72wb = models.BigIntegerField(blank=True, null=True)
    f_392sey8bgv6 = models.BigIntegerField(blank=True, null=True)
    f_n6vgqi8geyd = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'AttachedDocument'
