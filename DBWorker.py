import sqlite3


class DBWork:
    def __init__(self):
        self.con = sqlite3.connect('data/parameters.db')
        self.cur = self.con.cursor()

    def reset_game(self):
        if not self.is_save():
            self.cur.execute("INSERT INTO saveinfo(location, coord_x, coord_y) VALUES ('house', 6, 7)")
        else:
            self.cur.execute("UPDATE saveinfo SET location = 'house', coord_x = 6, coord_y = 7")
        self.con.commit()

    def save_game(self, loc, coord):
        self.cur.execute(f"UPDATE saveinfo SET location = '{loc}', coord_x = {coord[0]}, coord_y = {coord[1]}")
        self.con.commit()

    def is_save(self):
        return len(self.cur.execute("SELECT * from saveinfo").fetchall()) == 1

    def get_coord(self):
        return self.cur.execute('SELECT coord_x, coord_y FROM saveinfo').fetchone()

    def get_info_about_class(self, hero_class):
        return self.cur.execute(f'SELECT description FROM classinfo WHERE class="{hero_class}"').fetchone()[0]

    def get_location(self):
        return self.cur.execute('SELECT location FROM saveinfo').fetchone()[0]

    def get_all_info(self):
        return self.cur.execute('SELECT * FROM saveinfo').fetchone()