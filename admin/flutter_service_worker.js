'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';

const RESOURCES = {"version.json": "687edc4f4d548c8d671c11637730594d",
"index.html": "fc01563eeab5d8911738bb2c65e74d20",
"/": "fc01563eeab5d8911738bb2c65e74d20",
"main.dart.js": "79507284cf33517304086d5d413f8f7c",
"flutter.js": "c71a09214cb6f5f8996a531350400a9a",
"favicon.png": "5dcef449791fa27946b3d35ad8803796",
"icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
"icons/Icon-maskable-192.png": "c457ef57daa1d16f64b27b786ec2ea3c",
"icons/Icon-maskable-512.png": "301a7604d45b3e739efc881eb04896ea",
"icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
"manifest.json": "93027845378c2fe95a00fcd34103b408",
"Archive.zip": "dd8f92763078cf6cedccf68357001537",
"assets/images/settinglogo.png": "fdc65e9ddfb689c60d067b2aa005f197",
"assets/images/profile.svg": "d216fcd4a0fd548286a7038e03bb168d",
"assets/images/profile1.jpg": "99d6d63b4d94d1d1593ac6cd86612fd1",
"assets/images/personal.png": "b8b388de420a433ee5f77193a1c922c9",
"assets/AssetManifest.json": "552454578112758d3418b7f2ef541882",
"assets/NOTICES": "936ca0520b177eb7263add5b983874d3",
"assets/FontManifest.json": "e602cd0bc218fc810989b313ae9e98ae",
"assets/AssetManifest.bin.json": "5311836c119a2790e12b0aa9c3748dbe",
"assets/icons/Search.svg": "58814412c0fd36f2a731a335f17d9038",
"assets/icons/task.svg": "c2bdffd8ed67031951f00976b0575f6b",
"assets/icons/payment.svg": "e596b2f144e82e23a1024e087f05b9fb",
"assets/icons/sendp.svg": "c05c057cc884564053f2832b0443d587",
"assets/icons/halfround.svg": "5d43d1a8f3b1a7db01cbcea0e5ff834c",
"assets/icons/USD.svg": "4880447c75ec96884af87eb23c91d5b5",
"assets/icons/formentsize.svg": "d9eed5ede159cec25450d5ead922c3d7",
"assets/icons/dots.svg": "95140eaf3498147376ba38f248658e41",
"assets/icons/chart.svg": "b8c4c1df62af21ed14687df52413abe1",
"assets/icons/Logo%2520facebook%25207.svg": "f25eea3b6365ac6e70f41562d974dd8d",
"assets/icons/4dots.svg": "8c6b9ec997297279824ab86091ab319f",
"assets/icons/dollar.svg": "cbb6a99704805b3e58b85ab07ef2585a",
"assets/icons/home.svg": "2eabafca7c10853696915308fd307f0c",
"assets/icons/m.png": "e2a0d81406a2c3c3af93ef42fba93789",
"assets/icons/mast.png": "3edf92936189920b4e007a49686d88be",
"assets/icons/export.svg": "7690d9ddfafc6c62794541ce47f5d9d8",
"assets/icons/graphDown.svg": "a9ee72a48ac9c1fe7f8dc20c974a59fa",
"assets/icons/stock.svg": "44470d3456f815efd8d7006607ffd997",
"assets/icons/sendb.svg": "49ef72e2b7f0b639151600e72e912673",
"assets/icons/round.svg": "3e62a290e6b3dee0eaef3df3a7d776ce",
"assets/icons/home01.svg": "ccb1319f20844c983e3a6a13087fc10e",
"assets/icons/Logo%2520instagram%25206.svg": "362e59c3330e9f97c8a7fc7d7354b015",
"assets/icons/edit_2.svg": "9a47b05b258dfeb6b0b506053252cc3b",
"assets/icons/paymentdecline.png": "b689aacecb4981ee872429220ea82b2c",
"assets/icons/line4.svg": "aa26299c2cc295a771e9e37cb4bb9fe4",
"assets/icons/order.svg": "6663f6616ab5132f74cceb01dc686034",
"assets/icons/googleform.svg": "638ed082392bd654d9902699b1f77d58",
"assets/icons/settings.svg": "83e406c63cc661d6ad2eaade4d7adad0",
"assets/icons/cart.svg": "bb223c8d71507fda4aa4868c4b2e67fd",
"assets/icons/updatemeeting.svg": "f86917929ef567f421db6f8881124c2d",
"assets/icons/eye01.svg": "4b132cda955f0f2f84317fac3bb39b5a",
"assets/icons/emoji.svg": "7f6267c0a771634a34ce17a2a64a1958",
"assets/icons/sales.svg": "6b4a713319eb43feb341bab149201146",
"assets/icons/pin.svg": "21c39e369957b5f96a1ad9e11f5a70ea",
"assets/icons/roundeye.svg": "08b67592ddf41e0be349930f1057dabf",
"assets/icons/roles.svg": "f6c0dc80fa03193003e615bc606ff449",
"assets/icons/visa.png": "0561879feca6087e890237e1dd1fc869",
"assets/icons/line3.svg": "e46262b9b756ed9ca60c42035a2cfd35",
"assets/icons/csv1.svg": "ff7a77d9f8c1b7d295d520d19f130fd9",
"assets/icons/flash.svg": "da626231497e75f3e739a9ba30a60f09",
"assets/icons/line2.svg": "aa26299c2cc295a771e9e37cb4bb9fe4",
"assets/icons/roundplus.svg": "21715628fccbf4746d027f4e3e52dce3",
"assets/icons/eweb.svg": "b3e762fe32adf891662597387bef2f1e",
"assets/icons/meeting.svg": "9620c57927a6274c556a04a7579a6deb",
"assets/icons/google01.svg": "860b244b6f46770db67889bb104dbcb4",
"assets/icons/roundemoji.svg": "62a9455a8353d2d4845905f7f412b0a1",
"assets/icons/plus.svg": "735e3e316f20a8eb83d2494dbfb02cac",
"assets/icons/line1.svg": "e46262b9b756ed9ca60c42035a2cfd35",
"assets/icons/email.svg": "d5b5e496aa20cd55ad47aa0e1636fe5d",
"assets/icons/solar_logout-2-outline.svg": "ea44229f6cc4fc8d7c759f220c87951c",
"assets/icons/slider.svg": "d5f2564114be58e8b94b7ab0b062a28a",
"assets/icons/delete2.svg": "e56f9252a03a76feda95febb7e678ea3",
"assets/icons/subscription.svg": "d5a0f4f8bdc992bcdfbfe91ff76820a2",
"assets/icons/orders.svg": "163ac81e99c850f0763c8bc2938ef0ee",
"assets/icons/mic.svg": "967c9a6f0368f25abb837f17028bc2f9",
"assets/icons/pro.svg": "81228c09b9b1f3975ef660327dd78d0c",
"assets/icons/Button.svg": "24a00c0d4cbe34d86f06b97fc34e3058",
"assets/icons/Copyright%25C2%25A92023.svg": "789844ac0d10c1fe644fe278fb2fb271",
"assets/icons/csv.svg": "c5551dd40fd3888ad98f44feb172ed7f",
"assets/icons/Setting.svg": "aea10882ce0e1319d3fa31574220cd86",
"assets/icons/xlsx.svg": "c30df190c846fa1779817475f542fe29",
"assets/icons/notification.svg": "e435dfb150fb4b24bba4991a7940f7be",
"assets/icons/article.svg": "ce889f942477b728b4075f9c626fdebf",
"assets/icons/facebook.svg": "74fdafd29df1ac36468c33a1cb3e1ca1",
"assets/icons/camera.svg": "18febc31d3e036596cf674bb3a25d15b",
"assets/icons/whatsapp.svg": "b2adfc195313ebd99c020a90844d53d1",
"assets/icons/google.svg": "b89f5b1724c76caf69be14b4d5503b31",
"assets/icons/pay.png": "2600fcbf7c0042a25bb09738e783dd5a",
"assets/icons/categories.svg": "ae2086e488c75b058f26f39e6386fc18",
"assets/icons/graphUp.svg": "0b9d9fb843943c6dc1715377e03f7665",
"assets/icons/redcross.svg": "a530192e773303c86134b0315654430a",
"assets/icons/try.svg": "ee387c04bde5cc2222a6ff8f2dce0b06",
"assets/icons/edit.svg": "753c1acb668d23300956b9118533c2fc",
"assets/icons/updated.svg": "3b9500f9ded5c7a58d5bde2251e69309",
"assets/icons/meeting1.svg": "8aae1845701c33d9d36a3250db3fef96",
"assets/icons/integrations.svg": "ab9c4447922a8311f8bc80b79bb4cce3",
"assets/icons/circularplus.svg": "dccb295eb0462cd837fecaf3586c01c9",
"assets/icons/pdf.svg": "27694312831dc83aa4c846ed94a54c08",
"assets/icons/Frame.svg": "f072605b10738bcc13bc497dedcbc8aa",
"assets/icons/delete.svg": "7e4491fc62e0d3557ab468009741d9f3",
"assets/icons/dollor.svg": "d002d93c3620ff5d9b44101c8923f058",
"assets/icons/call.svg": "db53eb322809c827c2801ae1f136da60",
"assets/icons/device.svg": "123f173ffe7ef79a8cfc948252d4b6b7",
"assets/icons/eye.svg": "4b132cda955f0f2f84317fac3bb39b5a",
"assets/icons/thanks.png": "50b9d5fc66721d64a340f5b219d25dd3",
"assets/icons/linkedin.svg": "884f233ca8beefd67de2423ad85cfe4c",
"assets/icons/view.svg": "b288d4623339d36bcf17e07514083178",
"assets/icons/sebdw.svg": "01e4ea9f78aba44ddde71d982acbbb0d",
"assets/icons/Arrowdropup.svg": "23a61dea3050d91c83a5479e858fabaa",
"assets/icons/pay.svg": "6e77230a82180430f3ac0d05f4b144ad",
"assets/icons/cross.svg": "1935ebf07f22da3e30ba2a720527707e",
"assets/icons/pin1.svg": "06c5b6ea02a936c4872bc8f4022ad3c0",
"assets/icons/Logo%2520twitter%25207.svg": "294542318de30b60cd01abbc5ee1d45f",
"assets/icons/camera.png": "62f51b62f9d56ecda511bf95d84f922d",
"assets/icons/date.svg": "a39a8890d861405425a4496086329814",
"assets/icons/employee.svg": "1864b7d4d7805f37b5d6c159f59b3cd3",
"assets/icons/ordershow.svg": "38f8dd420fa4365d6ec75c13a7972b30",
"assets/icons/pinkdot.svg": "f13bdefbe13ffa9a21501c70c1193851",
"assets/icons/Globe%25206.svg": "65656c668092cceb5b51303c888ba94e",
"assets/icons/Outword.svg": "f86917929ef567f421db6f8881124c2d",
"assets/icons/ind.svg": "bbb3fd00561d0031fd109ec983ce3115",
"assets/icons/photo.svg": "f5a3c17124481abc92a09ab2ceb4d480",
"assets/icons/print.svg": "cb5ac15262a01d7c31c17790e2a29d91",
"assets/icons/bluedot.svg": "14274e7cdc41736af94d40727edaf229",
"assets/icons/customer.svg": "45847436ad8e02572537847e1fdb6754",
"assets/icons/mdi-light_camcorder.svg": "11e32662f35610b87b02a7edd0137aaf",
"assets/icons/pdf1.svg": "e7970597518466aacdcae97233c97981",
"assets/packages/flutter_csc_picker/lib/assets/country.json": "11b8187fd184a2d648d6b5be8c5e9908",
"assets/packages/cupertino_icons/assets/CupertinoIcons.ttf": "89ed8f4e49bcdfc0b5bfc9b24591e347",
"assets/packages/csc_picker/lib/assets/country.json": "11b8187fd184a2d648d6b5be8c5e9908",
"assets/packages/quill_html_editor/assets/delete_row.png": "3a56332918794e49ffca20016948553d",
"assets/packages/quill_html_editor/assets/insert_column_left.png": "114e6cca4b2f60a5eaebe4e574f2c36d",
"assets/packages/quill_html_editor/assets/insert_table.png": "c8f041a07bc6b8e4010ccf93ba4c291d",
"assets/packages/quill_html_editor/assets/h1_dark.png": "aa135c261ba758a3990d4594d982104d",
"assets/packages/quill_html_editor/assets/insert_row_above.png": "80ae3856d5f7415d9957d9a1699ec782",
"assets/packages/quill_html_editor/assets/insert_column_right.png": "fb27c4e3cc557089f79dd1f0cc937d62",
"assets/packages/quill_html_editor/assets/insert_row_below.png": "cea46607b37038f71c0fec22341b80e4",
"assets/packages/quill_html_editor/assets/camera_roll_icon.png": "962f1d57cab7451d4b92b236b1993bd5",
"assets/packages/quill_html_editor/assets/scripts/quill_2.0.0_4_min.js": "3f4b931496920ee12125e575f1c15dfa",
"assets/packages/quill_html_editor/assets/delete_column.png": "62358bf5aa9ac7f18e2411e4a0c63f14",
"assets/packages/quill_html_editor/assets/delete_table.png": "37e148071ce0a306a27f296369e52f40",
"assets/packages/quill_html_editor/assets/edit_table.png": "6a51397f56e90d98ae0b46a2e359676f",
"assets/packages/quill_html_editor/assets/h2_dark.png": "037de75dfed94244b78e7493c6425586",
"assets/packages/sn_progress_dialog/images/cancel.png": "be94b63af32e39fabad56e2cab611b4b",
"assets/packages/sn_progress_dialog/images/completed.png": "4f4ec717f6bb773c80db76261bb367c3",
"assets/packages/appflowy_editor/assets/images/point.svg": "50c7d9067a4a84945f1d79640589f501",
"assets/packages/appflowy_editor/assets/images/checkmark.svg": "3dc55867deb579484c5702a79054bb0e",
"assets/packages/appflowy_editor/assets/images/clear.svg": "f74736135d3ee5656b916262104469d0",
"assets/packages/appflowy_editor/assets/images/case_sensitive.svg": "1f93577f39711359040ffde3d815fdc6",
"assets/packages/appflowy_editor/assets/images/link.svg": "d323cd62b3df10a342e8e78ca50bf4e1",
"assets/packages/appflowy_editor/assets/images/regex.svg": "31424cd1f827bb7f237cd8e56c58f941",
"assets/packages/appflowy_editor/assets/images/clear_highlight_color.svg": "0b35a31822656c53578fb91acdfacb31",
"assets/packages/appflowy_editor/assets/images/toolbar/underline.svg": "fc86b2c49c42f5b9322a4ba76d066203",
"assets/packages/appflowy_editor/assets/images/toolbar/text_direction_ltr.svg": "16a42742a29ea1cf30253cd9429095cd",
"assets/packages/appflowy_editor/assets/images/toolbar/highlight_color.svg": "f8dd55016252c335c33e97fb39159882",
"assets/packages/appflowy_editor/assets/images/toolbar/strikethrough.svg": "82564a24aa7e82675d377431ac8fb075",
"assets/packages/appflowy_editor/assets/images/toolbar/divider.svg": "b7677e94ef1007c39a1853588b177d1e",
"assets/packages/appflowy_editor/assets/images/toolbar/link.svg": "42aee34d22fd39e710e4e448bf654e29",
"assets/packages/appflowy_editor/assets/images/toolbar/code.svg": "2d41f509ac1e1b1eb60c9adedc75ce03",
"assets/packages/appflowy_editor/assets/images/toolbar/bold.svg": "51e86ea040233e6a093caf02eea0c5f4",
"assets/packages/appflowy_editor/assets/images/toolbar/text.svg": "2b52bcda2b12945b27e859c414ef43c9",
"assets/packages/appflowy_editor/assets/images/toolbar/right.svg": "19968f066c5bccae9f3e059f04492850",
"assets/packages/appflowy_editor/assets/images/toolbar/text_color.svg": "b912db1bb9568af27b19e2946e38cf38",
"assets/packages/appflowy_editor/assets/images/toolbar/bulleted_list.svg": "b9441734387d7df0122b9dc629ca6bbb",
"assets/packages/appflowy_editor/assets/images/toolbar/numbered_list.svg": "a6072f727ea30c379dd5e0e2909790c4",
"assets/packages/appflowy_editor/assets/images/toolbar/text_direction_rtl.svg": "a994493865a43a16af27155434be4a6c",
"assets/packages/appflowy_editor/assets/images/toolbar/h1.svg": "735f59f34690e55680453a0d018ada75",
"assets/packages/appflowy_editor/assets/images/toolbar/h2.svg": "bf7b09c579a5db9e6392b01f95909347",
"assets/packages/appflowy_editor/assets/images/toolbar/italic.svg": "b96a655409eea41190182ae3ab3ed500",
"assets/packages/appflowy_editor/assets/images/toolbar/center.svg": "c44cf79c7fae101e6fb9daa8aaf62a54",
"assets/packages/appflowy_editor/assets/images/toolbar/h3.svg": "30d4699894d5de3b696b11cf678b35a0",
"assets/packages/appflowy_editor/assets/images/toolbar/quote.svg": "7d20ee07b7f80cc886294a43a0db0b3d",
"assets/packages/appflowy_editor/assets/images/toolbar/left.svg": "511106ad3206b6ccbf9702f22b0097db",
"assets/packages/appflowy_editor/assets/images/toolbar/text_direction_auto.svg": "74b07c6cd726be519ea32060d7a4b78c",
"assets/packages/appflowy_editor/assets/images/check.svg": "c7b016041b6a5b0ce7cd50b7277364ec",
"assets/packages/appflowy_editor/assets/images/copy.svg": "8aff328e13b4b3667a6fbe1046d691b2",
"assets/packages/appflowy_editor/assets/images/uncheck.svg": "d94aa89207d28adebb0a4e11237f1c57",
"assets/packages/appflowy_editor/assets/images/reset_text_color.svg": "a9ecce95365f0b4636ad43cc054d87e4",
"assets/packages/appflowy_editor/assets/images/image_toolbar/divider.svg": "b7677e94ef1007c39a1853588b177d1e",
"assets/packages/appflowy_editor/assets/images/image_toolbar/align_left.svg": "fcd2f1a9124961798dd7009f27172a64",
"assets/packages/appflowy_editor/assets/images/image_toolbar/copy.svg": "8aff328e13b4b3667a6fbe1046d691b2",
"assets/packages/appflowy_editor/assets/images/image_toolbar/align_right.svg": "bf18d4c1654d502abea1d2c8aa010c30",
"assets/packages/appflowy_editor/assets/images/image_toolbar/delete.svg": "15cbb502f4554ee7a443207099cc839a",
"assets/packages/appflowy_editor/assets/images/image_toolbar/share.svg": "42aee34d22fd39e710e4e448bf654e29",
"assets/packages/appflowy_editor/assets/images/image_toolbar/align_center.svg": "e82165a5f6fb20a7ad3a6faf0ab735cc",
"assets/packages/appflowy_editor/assets/images/upload_image.svg": "67fac764479d7cded5e98f6fe58c75ef",
"assets/packages/appflowy_editor/assets/images/delete.svg": "4a8d17ccc8cd1bd44a472f66ad028a01",
"assets/packages/appflowy_editor/assets/images/quote.svg": "ba6e97b8ddde8bf842fe2a56d06003ad",
"assets/packages/appflowy_editor/assets/images/selection_menu/number.svg": "9dad0889a48bb8f0ff288a5c0b711ab4",
"assets/packages/appflowy_editor/assets/images/selection_menu/text.svg": "890a3a1b0a674b1fbd769f42520cfef7",
"assets/packages/appflowy_editor/assets/images/selection_menu/image.svg": "92468547c1be63604f0820e565a1a6c2",
"assets/packages/appflowy_editor/assets/images/selection_menu/bulleted_list.svg": "7b22749438c843bc176fb559c924ad21",
"assets/packages/appflowy_editor/assets/images/selection_menu/checkbox.svg": "b81c986f918f1bd859fe07717b1e9d59",
"assets/packages/appflowy_editor/assets/images/selection_menu/h1.svg": "8135d2d5883f5cdd8776dca2dddb5f9b",
"assets/packages/appflowy_editor/assets/images/selection_menu/h2.svg": "129cb4e93b4badba4805968b13d52098",
"assets/packages/appflowy_editor/assets/images/selection_menu/h3.svg": "cd75480a77da1cabc7c5c2bf81325322",
"assets/packages/appflowy_editor/assets/images/selection_menu/quote.svg": "f58d378109520a8058edb4fed9d9ddbb",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/underline.svg": "472439a97df9c883661d818045a40d95",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/list.svg": "ed5fb52546835a9865541c1e2c06c20c",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/heading.svg": "8e872c0f97c1740a2f9858523aeb7743",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/strikethrough.svg": "c82d154453ef6759daa7cebb397cf58c",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/divider.svg": "098194a544d649f3545d35f301b0191f",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/link.svg": "d7a05e0d3a904118900ca7d8e3cf47b4",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/code.svg": "02ef07d8ea084d72dc2f4cc74a1b756d",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/text_decoration.svg": "e4dd4997dec353c1eb7cdfab039a49ef",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/bold.svg": "7118c4686f95cedaa776faf7924c89a0",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/close.svg": "aa945f43dcd92bce9b5c810eb33940be",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/setting.svg": "0cb728ff605b6f7457950f3a47d291f1",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/bulleted_list.svg": "4d7dba759b6073003a84e5938aa043b2",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/numbered_list.svg": "1daa60662c6ab43e65ac96e9e930b745",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/checkbox.svg": "eda1fb784a3429e96b42b7f24b7ea4c9",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/h1.svg": "295c462eeb57150f11a2e747d9220869",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/h2.svg": "88278b54319f416c66c1cf830fcf6c42",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/italic.svg": "c8585c2f19414f94f26430e8eecc4bb3",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/color.svg": "d061328f2a2b335e121c44dccff39a43",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/h3.svg": "ba38c1cdee5d41663df86128b73b835e",
"assets/packages/appflowy_editor/assets/mobile/toolbar_icons/quote.svg": "dda6772a0e0d9b40e8aad07ff377ffc1",
"assets/shaders/ink_sparkle.frag": "ecc85a2e95f5e9f53123dcaf8cb9b6ce",
"assets/AssetManifest.bin": "768b68a56864043a4871982f2b8bdf36",
"assets/fonts/Epilogue-Regular.ttf": "2c092196a0c31438829ac67a5bd07255",
"assets/fonts/MaterialIcons-Regular.otf": "1f11fc6c590c1bd3639904cf55bd946d",
"canvaskit/skwasm.js": "445e9e400085faead4493be2224d95aa",
"canvaskit/skwasm.js.symbols": "741d50ffba71f89345996b0aa8426af8",
"canvaskit/canvaskit.js.symbols": "38cba9233b92472a36ff011dc21c2c9f",
"canvaskit/skwasm.wasm": "e42815763c5d05bba43f9d0337fa7d84",
"canvaskit/chromium/canvaskit.js.symbols": "4525682ef039faeb11f24f37436dca06",
"canvaskit/chromium/canvaskit.js": "43787ac5098c648979c27c13c6f804c3",
"canvaskit/chromium/canvaskit.wasm": "f5934e694f12929ed56a671617acd254",
"canvaskit/canvaskit.js": "c86fbd9e7b17accae76e5ad116583dc4",
"canvaskit/canvaskit.wasm": "3d2a2d663e8c5111ac61a46367f751ac",
"canvaskit/skwasm.worker.js": "bfb704a6c714a75da9ef320991e88b03"};
// The application shell files that are downloaded before a service worker can
// start.
const CORE = ["main.dart.js",
"index.html",
"assets/AssetManifest.bin.json",
"assets/FontManifest.json"];

// During install, the TEMP cache is populated with the application shell files.
self.addEventListener("install", (event) => {
  self.skipWaiting();
  return event.waitUntil(
    caches.open(TEMP).then((cache) => {
      return cache.addAll(
        CORE.map((value) => new Request(value, {'cache': 'reload'})));
    })
  );
});
// During activate, the cache is populated with the temp files downloaded in
// install. If this service worker is upgrading from one with a saved
// MANIFEST, then use this to retain unchanged resource files.
self.addEventListener("activate", function(event) {
  return event.waitUntil(async function() {
    try {
      var contentCache = await caches.open(CACHE_NAME);
      var tempCache = await caches.open(TEMP);
      var manifestCache = await caches.open(MANIFEST);
      var manifest = await manifestCache.match('manifest');
      // When there is no prior manifest, clear the entire cache.
      if (!manifest) {
        await caches.delete(CACHE_NAME);
        contentCache = await caches.open(CACHE_NAME);
        for (var request of await tempCache.keys()) {
          var response = await tempCache.match(request);
          await contentCache.put(request, response);
        }
        await caches.delete(TEMP);
        // Save the manifest to make future upgrades efficient.
        await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
        // Claim client to enable caching on first launch
        self.clients.claim();
        return;
      }
      var oldManifest = await manifest.json();
      var origin = self.location.origin;
      for (var request of await contentCache.keys()) {
        var key = request.url.substring(origin.length + 1);
        if (key == "") {
          key = "/";
        }
        // If a resource from the old manifest is not in the new cache, or if
        // the MD5 sum has changed, delete it. Otherwise the resource is left
        // in the cache and can be reused by the new service worker.
        if (!RESOURCES[key] || RESOURCES[key] != oldManifest[key]) {
          await contentCache.delete(request);
        }
      }
      // Populate the cache with the app shell TEMP files, potentially overwriting
      // cache files preserved above.
      for (var request of await tempCache.keys()) {
        var response = await tempCache.match(request);
        await contentCache.put(request, response);
      }
      await caches.delete(TEMP);
      // Save the manifest to make future upgrades efficient.
      await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
      // Claim client to enable caching on first launch
      self.clients.claim();
      return;
    } catch (err) {
      // On an unhandled exception the state of the cache cannot be guaranteed.
      console.error('Failed to upgrade service worker: ' + err);
      await caches.delete(CACHE_NAME);
      await caches.delete(TEMP);
      await caches.delete(MANIFEST);
    }
  }());
});
// The fetch handler redirects requests for RESOURCE files to the service
// worker cache.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== 'GET') {
    return;
  }
  var origin = self.location.origin;
  var key = event.request.url.substring(origin.length + 1);
  // Redirect URLs to the index.html
  if (key.indexOf('?v=') != -1) {
    key = key.split('?v=')[0];
  }
  if (event.request.url == origin || event.request.url.startsWith(origin + '/#') || key == '') {
    key = '/';
  }
  // If the URL is not the RESOURCE list then return to signal that the
  // browser should take over.
  if (!RESOURCES[key]) {
    return;
  }
  // If the URL is the index.html, perform an online-first request.
  if (key == '/') {
    return onlineFirst(event);
  }
  event.respondWith(caches.open(CACHE_NAME)
    .then((cache) =>  {
      return cache.match(event.request).then((response) => {
        // Either respond with the cached resource, or perform a fetch and
        // lazily populate the cache only if the resource was successfully fetched.
        return response || fetch(event.request).then((response) => {
          if (response && Boolean(response.ok)) {
            cache.put(event.request, response.clone());
          }
          return response;
        });
      })
    })
  );
});
self.addEventListener('message', (event) => {
  // SkipWaiting can be used to immediately activate a waiting service worker.
  // This will also require a page refresh triggered by the main worker.
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
    return;
  }
  if (event.data === 'downloadOffline') {
    downloadOffline();
    return;
  }
});
// Download offline will check the RESOURCES for all files not in the cache
// and populate them.
async function downloadOffline() {
  var resources = [];
  var contentCache = await caches.open(CACHE_NAME);
  var currentContent = {};
  for (var request of await contentCache.keys()) {
    var key = request.url.substring(origin.length + 1);
    if (key == "") {
      key = "/";
    }
    currentContent[key] = true;
  }
  for (var resourceKey of Object.keys(RESOURCES)) {
    if (!currentContent[resourceKey]) {
      resources.push(resourceKey);
    }
  }
  return contentCache.addAll(resources);
}
// Attempt to download the resource online before falling back to
// the offline cache.
function onlineFirst(event) {
  return event.respondWith(
    fetch(event.request).then((response) => {
      return caches.open(CACHE_NAME).then((cache) => {
        cache.put(event.request, response.clone());
        return response;
      });
    }).catch((error) => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response != null) {
            return response;
          }
          throw error;
        });
      });
    })
  );
}
