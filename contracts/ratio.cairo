%lang starknet
%builtins pedersen range_check ecdsa

from starkware.cairo.common.registers import get_fp_and_pc
from starkware.cairo.common.cairo_builtins import HashBuiltin, SignatureBuiltin

##########
# STRUCTS
##########

#n -> numerator
#d -> denominator
struct Ratio:
    member n: felt
    member d: felt
end

##########
# MATH
##########

#x * y where x and y in rationals return z in rationals
@view
func ratio_mul{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }(x: Ratio, y: Ratio) -> (z: Ratio):
    alloc_locals
    
    # needed for dereferencing ratios
    let (__fp__, _) = get_fp_and_pc()

    return (Ratio(x.n * y.n, x.d * y.d))
end

@view
func ratio_div{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }(x: Ratio, y: Ratio) -> (z: Ratio):
    alloc_locals
    
    # needed for dereferencing ratios
    let (__fp__, _) = get_fp_and_pc()

    return (Ratio(x.n * y.d, x.d * y.n))
end

#x^m where x is element of rationals and m is element of naturals -> element of rationals
func ratio_pow{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }(x: Ratio, m: felt) -> (z: Ratio):
    alloc_locals

    if m == 0:
        return (Ratio(1, 1))
    end

    # needed for dereferencing ratios
    let (__fp__, _) = get_fp_and_pc()

    let rest_of_product: Ratio = ratio_pow(x, m - 1)
    let z: Ratio = ratio_mul(x, rest_of_product)

    return (z)
end

#x^1/m where x = a/b with a and b in Z mod p and m in Z mod p
@view
func ratio_nth_root{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }(x: Ratio, m: felt, error: Ratio) -> (z: Ratio):
    alloc_locals

    # needed for dereferencing ratios
    let (__fp__, _) = get_fp_and_pc()

    # divide by 2
    let candidate_root: Ratio = ratio_div(x, Ratio(2, 1))


func _less_than_error{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }(base_ratio: Ratio, candidate_root: Ratio, m: felt, error: felt) -> (bool: felt):
    alloc_locals

    # needed for dereferencing ratios
    let (__fp__, _) = get_fp_and_pc()

    let candidate_root_raised_to_m: Ratio = ratio_pow(candidate_root, m)
    
    #ratio_diff is defined to check which input is larger and substract smaller from larger
    let difference: Ratio = ratio_diff(base_ratio, candidate_root_raised_to_m)

    if difference < error:
        return (1)
    end

    return (0)



