/* total_charges*/
with charges_paid as (
    select 
        c.account_number,
        sum(c.value) as paid,
        count(c.status) as num_paid
    from 
        charges c
    where 
        c.status = 'paid'
    group by
        c.account_number
), charges_unpaid as (
    select 
        c.account_number,
        sum(c.value) as unpaid,
        count(c.status) as num_unpaid
    from 
        charges c
    where 
        c.status = 'unpaid'
    group by
        c.account_number
), total_charges as (
    select 
        cp.account_number, 
        cp.paid, 
        cp.num_paid,
        cu.unpaid,
        cu.num_unpaid
    from 
        charges_paid as cp inner join charges_unpaid as cu on (cp.account_number = cu.account_number)
)

select * from total_charges;

/*-----------------------------------------------------*/
/* total_transactions*/
with total_transactions as (
select 
    t.account_number,
    t.transaction_type_id,
    sum(t.value) as total_transaction,
    count(t.transaction_type_id) as num_transaction
from 
    transactions t 
group by
    t.account_number,
    t.transaction_type_id
), total_transactions_type as (
select 
    tt.account_number,
    tt.total_transaction,
    tt.num_transaction, 
    ty.description
from total_transactions tt left join transaction_type ty on (tt.transaction_type_id = ty.id)
)

select * from total_transactions_type;

/*-----------------------------------------------------*/
/*Account and address*/
select 
    ac.account_number,
    ac.birth,
    ac.occupation,
    ac.created_at as account_date,
    ad.state,
    ad.city,
    ad.created_at as address_date,
    l."level" 
from accounts ac left join address ad on (ac.address_id = ad.id)
    left join levels l on (ac.account_number = l.account_number);
/*--------------------------------------------------------*/