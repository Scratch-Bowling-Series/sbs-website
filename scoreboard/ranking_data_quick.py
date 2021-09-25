from scoreboard.rank_data import load_rank_data


def get_top_rankings(amount):
    rank_datas = load_rank_data()
    if rank_datas != None:
        return rank_datas[:amount]


