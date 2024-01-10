from simplegram import SG

from simplegram.controllers.auth import *
from simplegram.controllers.post import *

SG.route('/')(index)
SG.route('/addpost', methods=['GET', 'POST'])(add_post)
SG.route('/editpost/<post_id>', methods=['GET', 'POST'])(edit_post)
SG.route('/delpost/<post_id>')(del_post)
SG.route('/api/comments/<post_id>')(api_comments)

SG.route('/addcomment/<post_id>', methods=['GET', 'POST'])(add_comment)

SG.route('/login')(login)
SG.route('/login', methods=['POST'])(login_post)
SG.route('/logout')(logout)
SG.route('/register')(register)
SG.route('/register', methods=['POST'])(register_post)
SG.route('/reset_password')(reset_password)
SG.route('/reset_password', methods=['POST'])(reset_password_post)

SG.route('/myprofile')(my_profile)
SG.route('/myprofile', methods=['POST'])(my_profile_post)

SG.route('/mypost')(my_post)
