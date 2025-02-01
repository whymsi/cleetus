import discord
import aiosqlite

async def get_prefix(bot, message):
    try:
        async with aiosqlite.connect("prefixes.db") as db:
            async with db.cursor() as cursor:
                # Attempt to fetch the prefix from the database
                await cursor.execute("SELECT prefix FROM prefixes WHERE guild = ?", (message.guild.id,))
                data = await cursor.fetchone()
                
                if data:
                    return data[0]  # Return the custom prefix if found

                # If no prefix is found, insert the default prefix
                default_prefix = ','
                await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?, ?)', 
                                     (default_prefix, message.guild.id))
                await db.commit()  # Commit the transaction
                
                return default_prefix  # Return the default prefix
    except Exception as e:
        print(f"An error occurred: {e}")
        return ','  # Return default prefix in case of an error
                