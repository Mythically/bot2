# import asyncio
#
# from twitchio.ext import commands
# import sys
# from flask import Flask
# from flask import request
#
# app = Flask(__name__)
#
# if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#
#
# class api_cog(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     @app.route("/api", methods=["POST"])
#     def getData(self):
#         data = request.json
#         print(data)
#         return "", 200
#
#     @app.route("/zoomers")
#     async def zoomers(self):
#         self.bot.send_message()
#         return "200"
#
#     app.route("/get_my_ip", methods=["GET"])
#
#
# # def get_my_ip():
# #     return jsonify({"ip": request.remote_addr}), 200
#
# if __name__ == "__main__":
#     app.run()
# #     def prepare(self, bot: commands.Bot):
#         # Load our cog with this module...
#         # loop=asyncio.get_event_loop()
#         # loop.run_until_complete(app.run(host="localhost"), debug=True)
#         # bot.add_cog(api_cog(bot))
