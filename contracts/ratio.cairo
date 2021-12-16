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


