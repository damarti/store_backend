import graphene
from hashlib import md5
from graphene import relay
from graphene.relay.node import from_global_id
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from database.models import (db_session, ShopItemGroup as ShopItemGroupModel,
                             CurrentCost as CurrentCostModel,
                             HistoricalCost as HistoricalCostModel,
                             CorrectedCost as CorrectedCostModel,
                             NegotiatedDates as NegotiatedDatesModel,
                             GroupToItem as GroupToItemModel
)

class ShopItemGroup(SQLAlchemyObjectType):
    class Meta:
        model = ShopItemGroupModel
        interfaces = (relay.Node, )

class ShopItemGroupInput(graphene.InputObjectType):
    group_ud = graphene.String(required=True)
    rate_type = graphene.String(required=True)
    single_code = graphene.String(required=True)

class CreateShopItemGroup(graphene.Mutation):
    class Arguments:
        shop_item_group_data = ShopItemGroupInput(required=True)

    ok = graphene.Boolean()
    shop_item_group = graphene.Field(ShopItemGroup)

    @classmethod
    def mutate(cls, root, info, shop_item_group_data=None):
        new_shop_item_group = ShopItemGroupModel(
            group_ud = shop_item_group_data.group_ud,
            rate_type = shop_item_group_data.rate_type,
            single_code = shop_item_group_data.single_code,
            hash_key = md5(
                str(shop_item_group_data.group_ud).encode("utf-8") +
                str(shop_item_group_data.rate_type).encode("utf-8") +
                str(shop_item_group_data.single_code).encode("utf-8")
            ).hexdigest()
        )

        db_session.add(new_shop_item_group)
        db_session.commit()
        return CreateShopItemGroup(shop_item_group=new_shop_item_group, ok=True)

class DeleteShopItemGroupInput(graphene.InputObjectType):
    hash_key = graphene.String(required=True)

class DeleteShopItemGroup(graphene.Mutation):
    class Arguments:
        shop_item_group_data = DeleteShopItemGroupInput(required=True)
    
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, shop_item_group_data=None):
        shop_item_group = db_session.query(ShopItemGroupModel)\
            .filter_by(
                hash_key=shop_item_group_data.hash_key
            )
        shop_item_group.delete()
        db_session.commit()
        return DeleteShopItemGroup(ok=True)

class CurrentCost(SQLAlchemyObjectType):
    class Meta:
        model = CurrentCostModel
        interfaces = (relay.Node, )

class CurrentCostInput(graphene.InputObjectType):
    shop_item_group_id = graphene.ID(required=True)
    amount = graphene.Float(required=True)
    payment_type = graphene.String(required=True)

class CreateCurrentCost(graphene.Mutation):
    class Arguments:
        current_cost_data = CurrentCostInput(required=True)

    ok = graphene.Boolean()
    current_cost = graphene.Field(CurrentCost)

    @classmethod
    def mutate(cls, root, info, current_cost_data=None):
        new_current_cost = CurrentCostModel(
            shop_item_group_id = from_global_id(
                current_cost_data.shop_item_group_id
            )[1],
            amount = current_cost_data.amount,
            payment_type = current_cost_data.payment_type
        )

        db_session.add(new_current_cost)
        db_session.commit()
        return CreateCurrentCost(current_cost=new_current_cost, ok=True)

class DeleteCurrentCostInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

class DeleteCurrentCost(graphene.Mutation):
    class Arguments:
        current_cost_data = DeleteCurrentCostInput(required=True)
    
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, current_cost_data=None):
        current_cost = db_session.query(CurrentCostModel)\
            .filter_by(
                id=from_global_id(current_cost_data.id)[1]
            )
        current_cost.delete()
        db_session.commit()
        return DeleteCurrentCost(ok=True)

class HistoricalCost(SQLAlchemyObjectType):
    class Meta:
        model = HistoricalCostModel
        interfaces = (relay.Node, )

class HistoricalCostInput(graphene.InputObjectType):
    shop_item_group_id = graphene.ID(required=True)
    version_num = graphene.Int(required=True)
    amount = graphene.Float(required=True)
    payment_type = graphene.String(required=True)

class CreateHistoricalCost(graphene.Mutation):
    class Arguments:
        historical_cost_data = HistoricalCostInput(required=True)

    ok = graphene.Boolean()
    historical_cost = graphene.Field(HistoricalCost)

    @classmethod
    def mutate(cls, root, info, historical_cost_data=None):
        new_historical_cost = HistoricalCostModel(
            shop_item_group_id = from_global_id(
                historical_cost_data.shop_item_group_id
            )[1],
            version_num = historical_cost_data.version_num,
            amount = historical_cost_data.amount,
            payment_type = historical_cost_data.payment_type
        )

        db_session.add(new_historical_cost)
        db_session.commit()
        return CreateHistoricalCost(historical_cost=new_historical_cost, ok=True)

class DeleteHistoricalCostInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

class DeleteHistoricalCost(graphene.Mutation):
    class Arguments:
        historical_cost_data = DeleteHistoricalCostInput(required=True)
    
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, historical_cost_data=None):
        historical_cost = db_session.query(HistoricalCostModel)\
            .filter_by(
                id=from_global_id(historical_cost_data.id)[1]
            )
        historical_cost.delete()
        db_session.commit()
        return DeleteHistoricalCost(ok=True)

class CorrectedCost(SQLAlchemyObjectType):
    class Meta:
        model = CorrectedCostModel
        interfaces = (relay.Node, )

class CorrectedCostInput(graphene.InputObjectType):
    shop_item_group_id = graphene.ID(required=True)
    amount = graphene.Float(required=True)
    payment_type = graphene.String(required=True)

class CreateCorrectedCost(graphene.Mutation):
    class Arguments:
        corrected_cost_data = CorrectedCostInput(required=True)

    ok = graphene.Boolean()
    corrected_cost = graphene.Field(CorrectedCost)

    @classmethod
    def mutate(cls, root, info, corrected_cost_data=None):
        new_corrected_cost = CorrectedCostModel(
            shop_item_group_id = from_global_id(
                corrected_cost_data.shop_item_group_id
            )[1],
            amount = corrected_cost_data.amount,
            payment_type = corrected_cost_data.payment_type
        )

        db_session.add(new_corrected_cost)
        db_session.commit()
        return CreateCorrectedCost(corrected_cost=new_corrected_cost, ok=True)

class DeleteCorrectedCostInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

class DeleteCorrectedCost(graphene.Mutation):
    class Arguments:
        corrected_cost_data = DeleteCorrectedCostInput(required=True)
    
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, corrected_cost_data=None):
        corrected_cost = db_session.query(CorrectedCostModel)\
            .filter_by(
                id=from_global_id(corrected_cost_data.id)[1]
            )
        corrected_cost.delete()
        db_session.commit()
        return DeleteCorrectedCost(ok=True)

class NegotiatedDates(SQLAlchemyObjectType):
    class Meta:
        model = NegotiatedDatesModel
        interfaces = (relay.Node, )

class NegotiatedDatesInput(graphene.InputObjectType):
    legacy_group_ud = graphene.String(required=True)
    effective_start = graphene.Date(required=True)
    effective_end = graphene.Date(required=True)

class CreateNegotiatedDates(graphene.Mutation):
    class Arguments:
        new_negotiated_date = NegotiatedDatesInput(required=True)

    ok = graphene.Boolean()
    negotiated_date = graphene.Field(NegotiatedDates)

    @classmethod
    def mutate(cls, root, info, negotiated_date_data=None):
        new_negotiated_date = NegotiatedDatesModel(
            legacy_group_ud = negotiated_date_data.legacy_group_ud,
            effective_start = negotiated_date_data.effective_start,
            effective_end = negotiated_date_data.effective_end
        )

        db_session.add(new_negotiated_date)
        db_session.commit()
        return CreateNegotiatedDates(negotiated_date=new_negotiated_date, ok=True)

class DeleteNegotiatedDatesInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

class DeleteNegotiatedDates(graphene.Mutation):
    class Arguments:
        negotiated_date_data = DeleteNegotiatedDatesInput(required=True)
    
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, negotiated_date_data=None):
        negotiated_date = db_session.query(NegotiatedDatesModel)\
            .filter_by(
                id=from_global_id(negotiated_date_data.id)[1]
            )
        negotiated_date.delete()
        db_session.commit()
        return DeleteCurrentCost(ok=True)

class GroupToItem(SQLAlchemyObjectType):
    class Meta:
        model = GroupToItemModel
        interfaces = (relay.Node, )

class ARSMtoNPIInput(graphene.InputObjectType):
    group_ud = graphene.String(required=True)
    npi = graphene.String(required=True)

class CreateGroupToItem(graphene.Mutation):
    class Arguments:
        group_to_item_data = ARSMtoNPIInput(required=True)

    ok = graphene.Boolean()
    group_to_item = graphene.Field(GroupToItem)

    @classmethod
    def mutate(cls, root, info, group_to_item_data=None):
        new_group_to_item = GroupToItemModel(
            group_ud = group_to_item_data.group_ud,
            npi = group_to_item_data.npi
        )

        db_session.add(new_group_to_item)
        db_session.commit()
        return CreateGroupToItem(group_to_item=new_group_to_item, ok=True)

class DeleteGroupToItemInput(graphene.InputObjectType):
    id = graphene.ID(required=True)

class DeleteGroupToItem(graphene.Mutation):
    class Arguments:
        group_to_item_data = DeleteGroupToItemInput(required=True)
    
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, group_to_item_data=None):
        group_to_item = db_session.query(GroupToItemModel)\
            .filter_by(
                id=from_global_id(group_to_item_data.id)[1]
            )
        group_to_item.delete()
        db_session.commit()
        return DeleteGroupToItem(ok=True)

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    shop_item_group = relay.Node.Field(ShopItemGroup)
    current_cost = relay.Node.Field(CurrentCost)
    historical_cost = relay.Node.Field(HistoricalCost)
    corrected_cost = relay.Node.Field(CorrectedCost)
    negotiated_date = relay.Node.Field(NegotiatedDates)
    group_to_item = relay.Node.Field(GroupToItem)

    all_shop_item_groups = SQLAlchemyConnectionField(ShopItemGroup)
    all_current_costs = SQLAlchemyConnectionField(CurrentCost)
    all_historical_costs = SQLAlchemyConnectionField(HistoricalCost)
    all_corrected_costs = SQLAlchemyConnectionField(CorrectedCost)
    all_negotiated_dates = SQLAlchemyConnectionField(NegotiatedDates)
    all_group_to_item = SQLAlchemyConnectionField(GroupToItem)

    find_shop_item_group_by_hash = graphene.Field(ShopItemGroup, hash_key=graphene.String())

    def resolve_find_shop_item_group_by_hash(self, info, hash_key):
        query = ShopItemGroup.get_query(info)
        return query.filter(ShopItemGroupModel.hash_key == hash_key).first()

class Mutations(graphene.ObjectType):
    create_shop_item_group = CreateShopItemGroup.Field()
    create_current_cost = CreateCurrentCost.Field()
    create_historical_cost = CreateHistoricalCost.Field()
    create_corrected_cost = CreateCorrectedCost.Field()
    create_negotiated_date = CreateNegotiatedDates.Field()
    create_group_to_item = CreateGroupToItem.Field()

    delete_shop_item_group = DeleteShopItemGroup.Field()
    delete_current_cost = DeleteCurrentCost.Field()
    delete_historical_cost = DeleteHistoricalCost.Field()
    delete_corrected_cost = DeleteCorrectedCost.Field()
    delete_negotiated_date = DeleteNegotiatedDates.Field()
    delete_group_to_item = DeleteGroupToItem.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)