import pandas as pd
import random

def get_type_effectiveness():
    """Returns a dictionary representing the Pokémon type effectiveness chart."""
    return {
        'Normal': {'Rock': 0.5, 'Ghost': 0, 'Steel': 0.5},
        'Fire': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 2, 'Bug': 2, 'Rock': 0.5, 'Dragon': 0.5, 'Steel': 2},
        'Water': {'Fire': 2, 'Water': 0.5, 'Grass': 0.5, 'Ground': 2, 'Rock': 2, 'Dragon': 0.5},
        'Electric': {'Water': 2, 'Electric': 0.5, 'Grass': 0.5, 'Ground': 0, 'Flying': 2, 'Dragon': 0.5},
        'Grass': {'Fire': 0.5, 'Water': 2, 'Grass': 0.5, 'Poison': 0.5, 'Ground': 2, 'Flying': 0.5, 'Bug': 0.5, 'Rock': 2, 'Dragon': 0.5, 'Steel': 0.5},
        'Ice': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Ice': 0.5, 'Ground': 2, 'Flying': 2, 'Dragon': 2, 'Steel': 0.5},
        'Fighting': {'Normal': 2, 'Ice': 2, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 2, 'Ghost': 0, 'Dark': 2, 'Steel': 2, 'Fairy': 0.5},
        'Poison': {'Grass': 2, 'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0, 'Fairy': 2},
        'Ground': {'Fire': 2, 'Electric': 2, 'Grass': 0.5, 'Poison': 2, 'Flying': 0, 'Bug': 0.5, 'Rock': 2, 'Steel': 2},
        'Flying': {'Electric': 0.5, 'Grass': 2, 'Fighting': 2, 'Bug': 2, 'Rock': 0.5, 'Steel': 0.5},
        'Psychic': {'Fighting': 2, 'Poison': 2, 'Psychic': 0.5, 'Dark': 0, 'Steel': 0.5},
        'Bug': {'Fire': 0.5, 'Grass': 2, 'Fighting': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 2, 'Ghost': 0.5, 'Dark': 2, 'Steel': 0.5, 'Fairy': 0.5},
        'Rock': {'Fire': 2, 'Ice': 2, 'Fighting': 0.5, 'Ground': 0.5, 'Flying': 2, 'Bug': 2, 'Steel': 0.5},
        'Ghost': {'Normal': 0, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5},
        'Dragon': {'Dragon': 2, 'Steel': 0.5, 'Fairy': 0},
        'Dark': {'Fighting': 0.5, 'Psychic': 2, 'Ghost': 2, 'Dark': 0.5, 'Fairy': 0.5},
        'Steel': {'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Ice': 2, 'Rock': 2, 'Steel': 0.5, 'Fairy': 2},
        'Fairy': {'Fire': 0.5, 'Fighting': 2, 'Poison': 0.5, 'Dragon': 2, 'Dark': 2, 'Steel': 0.5}
    }

def calculate_damage(attacker, defender, type_chart):
    """Calculates damage based on stats and type effectiveness."""
    # Simplified damage formula
    damage = (attacker['Attack'] / defender['Defense']) * 50
    
    # Calculate type multiplier
    multiplier = 1
    type1_attacker = attacker['Type 1']
    type2_attacker = attacker['Type 2']
    
    type1_defender = defender['Type 1']
    type2_defender = defender['Type 2']
    
    if type1_defender in type_chart.get(type1_attacker, {}):
        multiplier *= type_chart[type1_attacker][type1_defender]
    if type2_defender and type2_defender in type_chart.get(type1_attacker, {}):
        multiplier *= type_chart[type1_attacker][type2_defender]
        
    # Sp. Atk could also be incorporated, but this is a good start
    
    return damage * multiplier

def simulate_battle(p1, p2, type_chart):
    """Simulates a turn-based battle until one Pokémon faints."""
    p1_hp = p1['HP']
    p2_hp = p2['HP']
    
    # Pokémon with higher speed attacks first
    turn = 1 if p1['Speed'] >= p2['Speed'] else 2
    
    while p1_hp > 0 and p2_hp > 0:
        if turn == 1:
            damage = calculate_damage(p1, p2, type_chart)
            p2_hp -= damage
            turn = 2
        else:
            damage = calculate_damage(p2, p1, type_chart)
            p1_hp -= damage
            turn = 1
            
    return 1 if p1_hp > 0 else 2

def main():
    print("Loading Pokémon data...")
    df = pd.read_csv('Pokemon/ML mode/pokemon_data.csv')
    df.rename(columns={'#': 'Number'}, inplace=True)
    
    type_chart = get_type_effectiveness()
    
    num_battles = 20000  # You can increase this for a more robust dataset
    battle_results = []
    
    print(f"Simulating {num_battles} battles...")
    
    for i in range(num_battles):
        # Select two different random Pokémon
        indices = random.sample(range(len(df)), 2)
        p1 = df.iloc[indices[0]]
        p2 = df.iloc[indices[1]]
        
        winner = simulate_battle(p1, p2, type_chart)
        
        # Randomly decide which Pokémon is 'pokemon_1' to avoid bias
        if random.random() < 0.5:
            pokemon_1 = p1
            pokemon_2 = p2
            # Winner is 0 if pokemon_1 wins, 1 if pokemon_2 wins
            result = 0 if winner == 1 else 1
        else:
            pokemon_1 = p2
            pokemon_2 = p1
            result = 1 if winner == 1 else 0

        battle_results.append({
            'p1_Name': pokemon_1['Name'],
            'p1_Type 1': pokemon_1['Type 1'],
            'p1_Type 2': pokemon_1['Type 2'],
            'p1_HP': pokemon_1['HP'],
            'p1_Attack': pokemon_1['Attack'],
            'p1_Defense': pokemon_1['Defense'],
            'p1_Speed': pokemon_1['Speed'],
            
            'p2_Name': pokemon_2['Name'],
            'p2_Type 1': pokemon_2['Type 1'],
            'p2_Type 2': pokemon_2['Type 2'],
            'p2_HP': pokemon_2['HP'],
            'p2_Attack': pokemon_2['Attack'],
            'p2_Defense': pokemon_2['Defense'],
            'p2_Speed': pokemon_2['Speed'],
            
            'Winner': result # 0 for p1, 1 for p2
        })

    results_df = pd.DataFrame(battle_results)
    results_df.to_csv('battle_data.csv', index=False)
    
    print(f"Simulation complete. 'battle_data.csv' created with {len(results_df)} results.")

if __name__ == "__main__":
    main()
