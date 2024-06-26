from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from website.models import Cart, CartItem   
from website import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def home():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    return render_template('cart.html', cart=cart)

@cart_bp.route('/cart/update_quantity', methods=['POST'])
@login_required
def update_quantity():
    item_id = request.form.get('item_id', type=int)
    new_quantity = request.form.get('quantity', type=int)

    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.cart.user_id != current_user.id:
        flash('You do not have permission to update this item.', 'danger')
        return redirect(url_for('cart.home'))

    cart_item.quantity = new_quantity
    db.session.commit()
    cart_item.cart.update_totals()
    return {'status': 'success', 'new_total': cart_item.cart.total_price}

@cart_bp.route('/cart/remove_item/<int:id>')
@login_required
def remove_item(id):
    cart_item = CartItem.query.get_or_404(id)
    if cart_item.cart.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'You do not have permission to remove this item.'}), 403
    
    cart = cart_item.cart
    db.session.delete(cart_item)
    db.session.commit()

    cart.update_totals()  # Cập nhật lại tổng số lượng và tổng giá của giỏ hàng
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Item removed from cart.'})