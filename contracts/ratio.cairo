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

    # if ratio in [0, 1)
    if x.n < x.d:
        let low_candidate: Ratio = x
        let high_candidate: Ratio = Ratio(1, 1)
    # if ratio in [1, ---]
    else:
        let low_candidate: Ratio = Ratio(1, 1)
        let high_candidate: Ratio = x
    end


    let z: Ratio = _recursion_nth_root(x, high_candidate, low_candidate, m, error)
    return (z)

func _recursion_nth_root{
        syscall_ptr : felt*,
        pedersen_ptr : HashBuiltin*,
        range_check_ptr
    }(base_ratio: Ratio, high_candidate: Ratio, low_candidate: Ratio, m: felt, error: Ratio) -> (nth_root: Ratio):
    # needed for dereferencing ratios
    let (__fp__, _) = get_fp_and_pc()

    let interval_sum: Ratio = ratio_add(high_candidate, low_candidate)
    let candidate_root: Ratio = ratio_div(interval_sum, Ratio(2,1))

    let less_than_error: felt = _less_than_error(base_ratio, candidate_root, m, error)

    if less_than_error == 1:
        return (candidate_root)
    else:
        if ratio_less_than(x, ratio_pow(candidate_root, m)):
            let new_high_candidate: Ratio = candidate_root
            let result: Ratio = _recursion_nth_root(base_ratio, new_high_candidate, low_candidate, m, error)

            return (result)
        else:
            let new_low_candidate: Ratio = candidate_root
            let result: Ratio = _recursion_nth_root(base_ratio, high_candidate, new_low_candidate, m, error)

            return (result)
        end
    end
end


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

    if ratio_less_than(difference, error):
        return (1)
    end

    return (0)
end

func ratio_add(first_ratio: Ratio, second_ratio: Ratio) -> (sum: Ratio):
    # needed for dereferencing ratios
    let (__fp__, _) = get_fp_and_pc()

    if first_ratio.d == second_ratio.d:
        let sum: Ratio = Ratio(first_ratio.n + second_ratio.n, first_ratio.d)
        return (sum)
    end

    let sum: Ratio = Ratio(first_ratio.n * second_ratio.d + second_ratio.n * first_ratio.d, first_ratio.d * second_ratio.d)
    return (sum)

func ratio_diff(base_ratio: Ratio, other_ratio: Ratio) -> (diff: Ratio):
    # needed for dereferencing ratios
    let (__fp__, _) = get_fp_and_pc()

    if base_ratio.d == other_ratio.d:
        if base_ratio.n > other_ratio.n:
            let diff: Ratio = Ratio(base_ratio.n - other_ratio.n, base_ratio.d)
            return (diff)
        else:
            let diff: Ratio = Ratio(other_ratio.n - base_ratio.n, base_ratio.d)
            return (diff)
        end
    end

    if base_ratio.n * other_ratio.d > other_ratio.n * base_ratio.d:
        let diff: Ratio = Ratio(base_ratio.n * other_ratio.d - other_ratio.n * base_ratio.d, base_ratio.d * other_ratio.d)
        return (diff)
    else:
        let diff: Ratio = Ratio(other_ratio.n * base_ratio.d - base_ratio.n * other_ratio.d, base_ratio.d * other_ratio.d)
        return (diff)
    end
end

func ratio_less_than(first_ratio: Ratio, second_ratio: Ratio) -> (bool: felt):
    # needed for dereferencing ratios
    let (__fp__, _) = get_fp_and_pc()

    if first_ratio.n * second_ratio.d < second_ratio.n * first_ratio.d:
        return (1)
    end

    return (0)
end



