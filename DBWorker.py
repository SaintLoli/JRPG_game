import sqlite3


class DBWork:
    def __init__(self):
        self.con = sqlite3.connect('data/parameters.db')
        self.cur = self.con.cursor()

    def reset_game(self, h1, h2, h3, h4):
        if not self.is_save():
            self.cur.execute(f"INSERT INTO saveinfo(location, coord_x, coord_y, hero1, hero2, hero3, hero4) VALUES ('house', 6, 7, '{h1}', '{h2}', '{h3}', '{h4}')")
        else:
            self.cur.execute(f"UPDATE saveinfo SET location = 'house', coord_x = 6, coord_y = 7, hero1 = '{h1}', hero2 = '{h2}', hero3 = '{h3}', hero4 = '{h4}'")
        self.con.commit()

    def save_game(self, loc, coord):
        self.cur.execute(f"UPDATE saveinfo SET location = '{loc}', coord_x = {coord[0]}, coord_y = {coord[1]}")
        self.con.commit()

    def is_save(self):
        return len(self.cur.execute("SELECT * from saveinfo").fetchall()) == 1

    def get_coord(self):
        return self.cur.execute('SELECT coord_x, coord_y FROM saveinfo').fetchone()

    def get_info_about_class(self, hero_class):
        return self.cur.execute(f'SELECT * FROM classinfo WHERE class="{hero_class}"').fetchone()

    def get_location(self):
        return self.cur.execute('SELECT location FROM saveinfo').fetchone()[0]

    def get_heroes(self):
        return self.cur.execute('SELECT hero1, hero2, hero3, hero4 from saveinfo').fetchone()

    def get_classes(self):
        return self.cur.execute('SELECT class FROM classinfo').fetchall()

    def get_attack_power(self, h_class):
        return self.cur.execute(f'SELECT min_atc, max_atc FROM classinfo WHERE class="{h_class}"').fetchone()

    def get_enemies_imgname(self):
        return self.cur.execute('SELECT imgname FROM enemies').fetchall()

    def get_enemies_gamename(self, imgname):
        return self.cur.execute(f'SELECT gamename FROM enemies WHERE imgname="{imgname}"')

    def get_all_about_enemy(self, imgname):
        return self.cur.execute(f'SELECT * FROM enemies WHERE imgname="{imgname}"').fetchone()

    def get_special_info(self, spec):
        return self.cur.execute(f'SELECT * FROM specialattacks WHERE special="{spec}"').fetchone()

    def set_HP(self, hero, HP):
        self.cur.execute(f'UPDATE aboutcharacters SET HP={HP} WHERE char_standart_name="{hero}"')
        self.con.commit()

    def set_about_characters(self, stand, pla_name, cl_name, id, HP, MP):
        if not self.is_save():
            self.cur.execute(
                f"INSERT INTO aboutcharacters(id, char_standart_name, char_player_name, class, HP, MP) VALUES ({id}, '{stand}', '{pla_name}', '{cl_name}', {HP}, {MP})")
        else:
            self.cur.execute(
                f"UPDATE aboutcharacters SET char_standart_name = '{stand}', char_player_name = '{pla_name}', class = '{cl_name}', HP={HP}, MP={MP} WHERE id = {id}")
        self.con.commit()

    def get_all_info_about_characters(self, st_name):
        return self.cur.execute(f'SELECT * FROM aboutcharacters WHERE char_standart_name = "{st_name}"').fetchone()